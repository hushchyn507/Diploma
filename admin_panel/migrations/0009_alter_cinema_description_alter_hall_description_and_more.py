# Generated by Django 4.1.3 on 2023-04-14 19:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0008_alter_hall_description_alter_page_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinema',
            name='description',
            field=models.TextField(max_length=500, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='description',
            field=models.TextField(max_length=500, validators=[django.core.validators.ProhibitNullCharactersValidator()], verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='news',
            name='description',
            field=models.TextField(max_length=500, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='news',
            name='short_description',
            field=models.TextField(max_length=50, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='page',
            name='description',
            field=models.TextField(max_length=500, validators=[django.core.validators.ProhibitNullCharactersValidator()], verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='page',
            name='description2',
            field=models.TextField(max_length=500, validators=[django.core.validators.ProhibitNullCharactersValidator()], verbose_name='Второе описание'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='description',
            field=models.TextField(max_length=500, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='short_description',
            field=models.TextField(max_length=50, validators=[django.core.validators.MaxLengthValidator(50), django.core.validators.RegexValidator('^[A-ZА-Я]{1}.*', message='Описание должно начинаться с заглавной буквы.'), django.core.validators.ProhibitNullCharactersValidator()], verbose_name='Краткое описание'),
        ),
    ]
