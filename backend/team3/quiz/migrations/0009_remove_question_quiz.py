# Generated by Django 2.1.7 on 2019-06-05 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_question_quiz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
    ]
