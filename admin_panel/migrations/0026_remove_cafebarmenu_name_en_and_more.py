# Generated by Django 4.1.3 on 2023-05-07 19:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0025_page_description2_en_page_description2_ru'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cafebarmenu',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='cafebarmenu',
            name='name_ru',
        ),
        migrations.AlterField(
            model_name='cafebarmenu',
            name='name',
            field=models.CharField(max_length=150, validators=[django.core.validators.MaxLengthValidator(150), django.core.validators.RegexValidator('^[A-ZА-Я]{1}.*', message='Название блюда должно начинаться с заглавной буквы'), django.core.validators.ProhibitNullCharactersValidator()], verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='scheme',
            field=models.ImageField(null=True, unique=True, upload_to='photos/%Y/%m/%d/', verbose_name='Схема зала'),
        ),
    ]
