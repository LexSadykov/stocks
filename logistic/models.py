from django.core.validators import MinValueValidator
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProductWarehouse(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    storage_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('product', 'warehouse')

    def __str__(self):
        return f'{self.product.name} in {self.warehouse.name}'