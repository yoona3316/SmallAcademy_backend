# Generated by Django 2.1.7 on 2019-05-31 12:33

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_articlemodel_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlemodel',
            name='important',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='file',
            field=models.FileField(null=True, upload_to=courses.models.upload_to),
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_name',
            field=models.CharField(max_length=20),
        ),
    ]