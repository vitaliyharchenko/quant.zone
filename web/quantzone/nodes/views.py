from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from lms.models import StudentLessonRelation, StudentTeacherRelation
from tasks.models import LessonTask

from results.models import (BlockResult, LessonResult,
                                   LessonResultBlockResultRelation)
from .models import Lesson


def perm_for_lesson(request, lesson):
    student_lessons = StudentLessonRelation.objects.filter(student=request.user, lesson=lesson)
    has_perm = False
    for student_lesson in student_lessons:
        if student_lesson.has_perm:
            has_perm = True
    if request.user.is_staff:
        has_perm = True
    return has_perm


@login_required
def lesson_view(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        # TODO: add 404 page
        pass

    if lesson.lesson_block_relations.count() == 0:
        messages.warning(request, "Это пустой урок")
        return_path = request.META.get('HTTP_REFERER', '/')
        return redirect(return_path)

    if perm_for_lesson(request, lesson):
        args = {'lesson': lesson}
        if request.user.is_teacher:
            student_teachers = StudentTeacherRelation.objects.filter(teacher=request.user)
            args['student_teachers'] = student_teachers
        return render(request, 'teaching/lesson.html', args)
    else:
        messages.warning(request, 'Нет доступа к уроку')
        return_path = request.META.get('HTTP_REFERER', '/')
        return redirect(return_path)


@login_required
def lesson_final_view(request, lesson_id):
    args = {}
    try:
        lesson = Lesson.objects.get(id=lesson_id)
        args['lesson'] = lesson

        summ = 0
        max_summ = 0

        lesson_result = LessonResult.objects.create(student=request.user, lesson=lesson, score=0, max_score=0)

        for lesson_block_relation in lesson.lesson_block_relations:
            block_result = BlockResult.objects.filter(block=lesson_block_relation.block, student=request.user).latest(
                'date')
            summ += block_result.score
            max_summ += block_result.max_score

            lesson_result_block_result_relation = LessonResultBlockResultRelation.objects.create(
                lesson_result=lesson_result, block_result=block_result)
            lesson_result_block_result_relation.save()

        lesson_result.score = summ
        lesson_result.max_score = max_summ
        lesson_result.save()

        args['lesson_result'] = lesson_result

        try:
            tasks = LessonTask.objects.filter(student=request.user, lesson=lesson, is_finished=False)
            for task in tasks:
                task.is_finished = True
                task.lesson_result = lesson_result
                task.save()
        except LessonTask.DoesNotExist:
            pass

        return render(request, 'teaching/lesson_final.html', args)
    except Lesson.DoesNotExist:
        # TODO: add 404 page
        messages.warning(request, "Такого объекта нет =(")
        return redirect('index_view')
