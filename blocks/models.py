from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_markdown.models import MarkdownField
from django.utils import timezone
from users.models import User


# All lessons contains blocks (text, chioce, question with float answer)
class Block(models.Model):

    def __str__(self):
        title = None

        try:
            title = self.textblock.title
        except AttributeError:
            pass

        try:
            title = self.choicequestion.question_text[:100]
        except AttributeError:
            pass

        try:
            title = self.floatquestion.question_text[:100]
        except AttributeError:
            pass

        if title:
            return title
        else:
            return u'Block #{}'.format(self.id)

    def get_absolute_url(self):
        return "/block/%i" % self.id


class TextBlock(Block):
    class Meta:
        verbose_name = 'текстовая статья'
        verbose_name_plural = 'текстовые статьи'

    title = models.CharField(max_length=200, unique=True)
    body = MarkdownField()

    def __str__(self):
        return self.title


class ChoiceBlock(Block):
    class Meta:
        verbose_name = 'тестовый вопрос'
        verbose_name_plural = 'тестовые вопросы'

    question_text = MarkdownField('Текст вопроса')
    image = models.ImageField('Картинка', upload_to='choice_blocks/', null=True, blank=True)

    def __str__(self):
        return self.question_text


class ChoiceBlockOption(models.Model):
    class Meta:
        verbose_name = 'Вариант ответа на тестовый вопрос'
        verbose_name_plural = 'Варианты ответа на тестовые вопросы'

    choice_block = models.ForeignKey(ChoiceBlock)
    option_text = models.CharField('Вариант ответа', max_length=600, blank=True)
    option_image = models.ImageField('Картинка', upload_to='choice_block_options/', null=True, blank=True)
    help_text = models.CharField('Подсказка', max_length=300, blank=True)
    is_true = models.BooleanField('Правильный?')

    def __str__(self):
        return self.option_text


class FloatBlock(Block):
    class Meta:
        verbose_name = 'задача с численным ответом'
        verbose_name_plural = 'задачи с численным ответом'

    question_text = MarkdownField('Текст вопроса')
    image = models.ImageField('Картинка', upload_to='float_questions/', null=True, blank=True)
    answer = models.FloatField('Ответ')

    def __str__(self):
        return self.question_text


# =================
# Results of blocks
# =================
class BlockResult(models.Model):
    class Meta:
        verbose_name = 'Результат ответа'
        verbose_name_plural = 'Результаты ответов'

    user = models.ForeignKey(User)
    block = models.ForeignKey(Block)
    date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField()

    def __str__(self):
        return u'{}, {}, {}'.format(self.user, self.block, self.date)


class ChoiceBlockResult(BlockResult):
    class Meta:
        verbose_name = 'Результат ответа на тестовый вопрос'
        verbose_name_plural = 'Результаты ответов на тестовые вопросы'

    choices = ArrayField(models.IntegerField())


class FloatBlockResult(BlockResult):
    class Meta:
        verbose_name = 'Результат ответа на задачу'
        verbose_name_plural = 'Результаты ответов на задачи'

    answer = models.FloatField('Ответ')


# Включение блоков в урок
class LessonBlockRelation(models.Model):
    class Meta:
        verbose_name = 'включение блока в урок'
        verbose_name_plural = 'включения блоков в урок'
        unique_together = ('lesson', 'block')

    lesson = models.ForeignKey('nodes.Lesson')
    block = models.ForeignKey(Block)
    order = models.IntegerField()
