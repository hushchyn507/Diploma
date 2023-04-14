# Generated by Django 4.1.3 on 2023-04-13 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0003_alter_templatehtml_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='budget',
            field=models.PositiveIntegerField(verbose_name='Бюджет'),
        ),
        migrations.AlterField(
            model_name='film',
            name='duration',
            field=models.PositiveSmallIntegerField(verbose_name='Длительность(минуты)'),
        ),
        migrations.AlterField(
            model_name='film',
            name='legal_age',
            field=models.PositiveSmallIntegerField(verbose_name='Мин Возраст'),
        ),
        migrations.AlterField(
            model_name='film',
            name='year',
            field=models.PositiveSmallIntegerField(verbose_name='Год'),
        ),
    ]
