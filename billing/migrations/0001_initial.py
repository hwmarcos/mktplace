# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 22:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('portal', '0006_auto_20170609_2055'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commission', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Refused', 'Refused'), ('Aproved', 'Aproved')], default='Pending', max_length=10)),
                ('shipment_status', models.CharField(choices=[('Pending', 'Pending'), ('Packing', 'Packing'), ('Posted', 'Posted'), ('Delivered', 'Delivered')], default='Pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchant', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product', to='portal.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
