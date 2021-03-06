# Generated by Django 3.1.5 on 2021-03-04 11:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MarketingMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=120)),
                ('active', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('end_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
    ]
