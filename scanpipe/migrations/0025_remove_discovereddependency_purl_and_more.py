# Generated by Django 4.0.6 on 2022-08-16 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scanpipe', '0024_migrate_dependency_uid_to_purl_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discoveredpackage',
            name='dependencies_data',
        ),
        migrations.RemoveField(
            model_name='discovereddependency',
            name='purl',
        ),
    ]
