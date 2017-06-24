from django.contrib.auth.models import User
from django.db import models

from portal.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, related_name='order_user')
    merchant = models.ForeignKey(User, related_name='merchant')
    product = models.ForeignKey(Product, related_name='order_product')
    commission = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Refused', 'Refused'),
        ('Approved', 'Approved'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='Pending')
    SHIPMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Packing', 'Packing'),
        ('Posted', 'Posted'),
        ('Delivered', 'Delivered'),
    )
    shipment_status = models.CharField(choices=SHIPMENT_STATUS_CHOICES, max_length=10, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return '#' + str(self.id)
