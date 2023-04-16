# Generated by Django 4.1.3 on 2023-04-16 06:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0012_alter_film_trailer_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='trailer_link',
            field=models.URLField(validators=[django.core.validators.URLValidator(message='XYZ'), django.core.validators.RegexValidator('https?:\\/\\/(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\x08([-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)', message='Неверный url адресс')], verbose_name='Ссылка на трейлер'),
        ),
    ]
