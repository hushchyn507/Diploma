# Generated by Django 4.1.3 on 2023-05-06 19:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0024_cafebarmenu_name_en_cafebarmenu_name_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='description2_en',
            field=models.TextField(max_length=10000, null=True, validators=[django.core.validators.MaxLengthValidator(10000), django.core.validators.RegexValidator('^[A-ZА-Я]{1}.*', message='Описание должно начинаться с заглавной буквы.'), django.core.validators.ProhibitNullCharactersValidator()], verbose_name='Второе описание'),
        ),
        migrations.AddField(
            model_name='page',
            name='description2_ru',
            field=models.TextField(max_length=10000, null=True, validators=[django.core.validators.MaxLengthValidator(10000), django.core.validators.RegexValidator('^[A-ZА-Я]{1}.*', message='Описание должно начинаться с заглавной буквы.'), django.core.validators.ProhibitNullCharactersValidator()], verbose_name='Второе описание'),
        ),
    ]