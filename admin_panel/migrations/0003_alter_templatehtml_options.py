# Generated by Django 4.1.3 on 2023-04-11 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_templatehtml'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='templatehtml',
            options={'ordering': ['-date_uploaded']},
        ),
    ]
