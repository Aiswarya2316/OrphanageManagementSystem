# Generated by Django 5.1.6 on 2025-03-24 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_delete_contactmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='children',
        ),
        migrations.AddField(
            model_name='event',
            name='conducted_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='event_images/'),
        ),
    ]
