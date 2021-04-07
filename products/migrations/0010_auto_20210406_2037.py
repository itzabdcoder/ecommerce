# Generated by Django 3.1.7 on 2021-04-06 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20210406_2008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, to='products.Category'),
        ),
    ]
