# Generated by Django 5.0.2 on 2024-02-15 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_userdetails_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='review',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
