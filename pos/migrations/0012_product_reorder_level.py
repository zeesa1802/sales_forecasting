# Generated by Django 3.2 on 2021-12-05 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0011_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reorder_level',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
