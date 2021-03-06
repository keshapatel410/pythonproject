# Generated by Django 2.2.6 on 2019-12-12 22:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='externalURL',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(0)]),
        ),
    ]
