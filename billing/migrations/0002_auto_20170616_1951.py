# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 22:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},
        ),
    ]
