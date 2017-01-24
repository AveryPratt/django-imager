# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-20 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='bio',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='camera',
            field=models.CharField(blank=True, choices=[('N', 'Nikon'), ('C', 'Canon'), ('K', 'Kodak')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='photography_type',
            field=models.CharField(blank=True, choices=[('LS', 'landscape'), ('PT', 'portrait'), ('NA', 'nature'), ('AS', 'astronomy')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='travel_radius',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='website',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]