# Generated by Django 5.1.4 on 2025-03-12 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('image_name', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('processed_at', models.DateTimeField(auto_now=True)),
                ('processed_image_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
