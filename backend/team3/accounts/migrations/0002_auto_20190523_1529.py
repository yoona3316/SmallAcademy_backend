# Generated by Django 2.1.7 on 2019-05-23 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
