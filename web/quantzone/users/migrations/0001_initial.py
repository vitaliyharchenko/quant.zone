# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 17:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('vkuserid', models.IntegerField(blank=True, null=True, unique=True)),
                ('b_date', models.DateField(help_text='В формате ДД.ММ.ГГГГ', verbose_name='Дата рождения')),
                ('first_name', models.CharField(max_length=120, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=120, verbose_name='Фамилия')),
                ('sex', models.CharField(choices=[('m', 'мужской'), ('f', 'женский')], max_length=1, verbose_name='Пол')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Доступ к админке')),
                ('is_teacher', models.BooleanField(default=False, verbose_name='Учитель')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
        ),
        migrations.CreateModel(
            name='UserActivation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_key', models.CharField(blank=True, max_length=100)),
                ('request_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('confirm_time', models.DateTimeField(blank=True, null=True, verbose_name='Дата активации')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Активациия пользователя',
                'verbose_name_plural': 'Активации пользователей',
            },
        ),
    ]
