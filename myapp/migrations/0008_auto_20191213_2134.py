# Generated by Django 2.2.6 on 2019-12-13 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20191213_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
    ]
