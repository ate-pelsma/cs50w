# Generated by Django 3.2.9 on 2022-01-07 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_new_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new_post',
            name='content',
            field=models.CharField(max_length=256),
        ),
    ]