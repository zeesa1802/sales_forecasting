# Generated by Django 3.2 on 2021-12-30 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0020_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_products_id',
            field=models.IntegerField(default=99),
            preserve_default=False,
        ),
    ]
