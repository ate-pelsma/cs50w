# Generated by Django 3.2.9 on 2022-01-07 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_new_post_content'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='New_Post',
            new_name='Post',
        ),
    ]
