# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataobjects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='name',
            field=models.SlugField(editable=False, unique=True),
        ),
    ]