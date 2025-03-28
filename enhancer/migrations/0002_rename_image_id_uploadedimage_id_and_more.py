# Generated by Django 5.1.7 on 2025-03-25 11:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enhancer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadedimage',
            old_name='image_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='uploadedimage',
            name='processed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='uploadedimage',
            name='uploaded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
