# Generated by Django 3.1b1 on 2020-08-21 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bjcl_app', '0003_auto_20200819_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='disp_color',
            field=models.CharField(default='orange', max_length=100),
        ),
    ]