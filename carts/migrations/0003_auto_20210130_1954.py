# Generated by Django 3.1.5 on 2021-01-30 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_auto_20210127_1945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='updated',
        ),
    ]
