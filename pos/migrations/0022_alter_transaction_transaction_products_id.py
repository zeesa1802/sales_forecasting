# Generated by Django 3.2 on 2021-12-30 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0021_transaction_transaction_products_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_products_id',
            field=models.CharField(max_length=1000),
        ),
    ]
