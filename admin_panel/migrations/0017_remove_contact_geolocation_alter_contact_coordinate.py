# Generated by Django 4.1.3 on 2023-04-30 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0016_contact_geolocation_alter_backimg_img_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='geolocation',
        ),
        migrations.AlterField(
            model_name='contact',
            name='coordinate',
            field=models.TextField(),
        ),
    ]
