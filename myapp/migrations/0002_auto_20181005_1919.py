# Generated by Django 2.1.2 on 2018-10-05 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dreamreal',
            old_name='mail',
            new_name='password',
        ),
        migrations.RemoveField(
            model_name='dreamreal',
            name='phonenumber',
        ),
        migrations.RemoveField(
            model_name='dreamreal',
            name='website',
        ),
    ]