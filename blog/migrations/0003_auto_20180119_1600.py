# Generated by Django 2.0 on 2018-01-19 16:00

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_upload'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique_for_date='publish'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='published', max_length=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.CharField(default='', max_length=50),
        ),
    ]
