# Generated by Django 3.1.5 on 2021-03-23 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210323_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='country',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
