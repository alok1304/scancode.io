# Generated by Django 4.2.1 on 2023-06-06 04:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scanpipe", "0032_scancode_toolkit_v32_post_data_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="project",
            name="settings",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]