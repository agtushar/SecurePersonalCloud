# Generated by Django 2.1.2 on 2018-10-20 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_remove_userfile_filepath'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfile',
            name='owners',
        ),
        migrations.AddField(
            model_name='myuser',
            name='files',
            field=models.ManyToManyField(to='storage.userFile'),
        ),
    ]