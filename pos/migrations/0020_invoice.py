# Generated by Django 3.2 on 2021-12-05 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0019_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('data', models.JSONField()),
            ],
        ),
    ]