# Generated by Django 5.0.2 on 2024-02-11 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_userdetails_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]
