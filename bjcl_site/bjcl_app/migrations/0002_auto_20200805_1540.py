# Generated by Django 3.1b1 on 2020-08-05 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bjcl_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Books',
            new_name='Book',
        ),
        migrations.RenameField(
            model_name='authors',
            old_name='Books',
            new_name='Book',
        ),
    ]
