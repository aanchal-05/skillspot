# Generated by Django 5.0.2 on 2024-02-19 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_userdetails_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]