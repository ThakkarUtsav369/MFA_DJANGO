# Generated by Django 4.0.5 on 2023-03-29 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='username',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
