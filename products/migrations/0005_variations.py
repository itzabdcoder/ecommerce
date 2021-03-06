# Generated by Django 3.1.5 on 2021-02-09 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20210125_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('size', 'size'), ('color', 'color')], default='size', max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField()),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productimage')),
            ],
        ),
    ]
