# Generated by Django 2.1.7 on 2019-06-16 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0019_auto_20190615_0330'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='wrong_answers',
            field=models.ManyToManyField(related_name='wrong_answers', to='quiz.Question'),
        ),
    ]
