# Generated by Django 4.0.5 on 2022-12-04 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0021_remove_page_posts_pageposts_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pageposts',
            name='page',
        ),
        migrations.AddField(
            model_name='page',
            name='posts',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pagepost', to='network.pageposts'),
        ),
    ]
