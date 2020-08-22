# Generated by Django 3.1b1 on 2020-08-21 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bjcl_app', '0010_delete_searchers'),
    ]

    operations = [
        migrations.CreateModel(
            name='searchers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(max_length=200)),
                ('ip', models.CharField(max_length=200)),
                ('browser_info', models.CharField(max_length=200)),
                ('device_info', models.CharField(max_length=500)),
                ('os_info', models.CharField(max_length=200)),
            ],
        ),
    ]
