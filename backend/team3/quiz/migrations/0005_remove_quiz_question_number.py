# Generated by Django 2.1.7 on 2019-06-05 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20190606_0135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='question_number',
        ),
    ]
