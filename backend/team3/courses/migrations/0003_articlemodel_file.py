# Generated by Django 2.1.7 on 2019-05-22 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20190506_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlemodel',
            name='file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]