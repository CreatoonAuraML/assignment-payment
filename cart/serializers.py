from rest_framework import serializers
from django.db import IntegrityError
from .models import User, Item, Order, ItemCategory, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.date_of_birth = validated_data.get(
            'date_of_birth', instance.date_of_birth)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        instance.save()

        return instance


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = '__all__'

    def validate_type(self, value):
        lowercased_type = value.lower()
        existing_category = ItemCategory.objects.filter(
            type=lowercased_type).first()
        if existing_category:
            raise serializers.ValidationError("Category already exists.")
        return value


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'created_at', 'brand', 'name',
                  'price', 'quantity', 'description', 'category']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        category = ItemCategorySerializer(instance.category).data
        data['category'] = category
        return data

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "Item with this name and brand already exists, Use different combination.")

    def update(self, instance, validated_data):
        category_id = validated_data.pop('category', None)
        try:
            instance = super().update(instance, validated_data)
            if category_id is not None:
                instance.category = category_id
                instance.save()
            return instance
        except IntegrityError:
            raise serializers.ValidationError(
                "Item with this name and brand already exists, Use different combination.")

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_status', 'order']

class OrderSerializer(serializers.ModelSerializer):

    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'currency', 'amount', 'date_time',
                  'items', 'user', 'payment']
        
    def create(self, validated_data):
        items_data = validated_data.pop('items')  
        payment_data = {'payment_status': 'processing'}

        order = Order.objects.create(**validated_data) 
        payment = Payment.objects.create(order=order, **payment_data)

        total_amount = 0 
        item_ids = []

        for item_data in items_data:
            item_ids.append(item_data.id)
            total_amount += item_data.price 

        order.items.set(item_ids)
        order.amount = total_amount  
        order.save()  

        return order
        
    def to_representation(self, instance):
        data = super().to_representation(instance)

        items_data = ItemSerializer(instance.items, many=True).data

        data['items'] = items_data

        return data
        
