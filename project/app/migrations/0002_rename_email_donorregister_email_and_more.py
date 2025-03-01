# Generated by Django 5.0.1 on 2025-02-04 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donorregister',
            old_name='Email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='donorregister',
            old_name='phonenumber',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='stafreg',
            old_name='Email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='stafreg',
            old_name='phonenumber',
            new_name='phone',
        ),
        migrations.AddField(
            model_name='donorregister',
            name='confirm_password',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stafreg',
            name='confirm_password',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
