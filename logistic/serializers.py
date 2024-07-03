from rest_framework import serializers
from .models import Product, Warehouse, ProductWarehouse

class ProductWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductWarehouse
        fields = ('product', 'warehouse', 'storage_cost')

class ProductSerializer(serializers.ModelSerializer):
    warehouses = ProductWarehouseSerializer(source='productwarehouse_set', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'warehouses')

    def create(self, validated_data):
        warehouses_data = self.context['request'].data.get('warehouses')
        product = Product.objects.create(**validated_data)
        for warehouse_data in warehouses_data:
            ProductWarehouse.objects.create(product=product, **warehouse_data)
        return product

    def update(self, instance, validated_data):
        warehouses_data = self.context['request'].data.get('warehouses')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        for warehouse_data in warehouses_data:
            ProductWarehouse.objects.update_or_create(
                product=instance,
                warehouse_id=warehouse_data['warehouse'],
                defaults={'storage_cost': warehouse_data['storage_cost']}
            )
        return instance

class WarehouseSerializer(serializers.ModelSerializer):
    products = ProductWarehouseSerializer(source='productwarehouse_set', many=True, read_only=True)

    class Meta:
        model = Warehouse
        fields = ('id', 'name', 'products')