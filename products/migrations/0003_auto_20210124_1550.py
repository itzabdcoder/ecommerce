# Generated by Django 3.1.5 on 2021-01-24 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210122_1604'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('title', 'slug')},
        ),
    ]
