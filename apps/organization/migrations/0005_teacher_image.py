# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-03-12 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20190306_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, upload_to='teacher/%Y/%m', verbose_name='\u6559\u5e08\u5f62\u8c61\u7167\u7247'),
        ),
    ]