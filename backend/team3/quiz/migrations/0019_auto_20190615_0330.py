# Generated by Django 2.1.7 on 2019-06-14 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0018_auto_20190615_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizbox',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='quizbox_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
