# Generated by Django 3.2.9 on 2021-12-08 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20211208_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.TextField(blank=True),
        ),
    ]
