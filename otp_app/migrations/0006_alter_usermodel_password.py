# Generated by Django 4.0.5 on 2023-03-29 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp_app', '0005_alter_usermodel_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
