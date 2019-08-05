# Generated by Django 2.1.7 on 2019-06-06 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_quiz_quizbox'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='quizbox',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='quiz.QuizBox'),
        ),
        migrations.AlterField(
            model_name='quizbox',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quizbox', to='courses.Course'),
        ),
    ]
