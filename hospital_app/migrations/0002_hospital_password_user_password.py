# Generated by Django 4.2.3 on 2023-10-30 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='password',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
