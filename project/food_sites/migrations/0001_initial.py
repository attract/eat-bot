# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-31 12:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dynamic_scraper', '0026_auto_20180331_0822'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('weight', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='files/food_sites/images/', verbose_name='Фото')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('url', models.URLField()),
                ('checker_runtime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dynamic_scraper.SchedulerRuntime')),
            ],
        ),
        migrations.CreateModel(
            name='FoodWebsite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('scraper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dynamic_scraper.Scraper')),
                ('scraper_runtime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dynamic_scraper.SchedulerRuntime')),
            ],
        ),
        migrations.AddField(
            model_name='foodproduct',
            name='food_website',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_sites.FoodWebsite'),
        ),
    ]
