from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_email(self, obj):
        return obj.user.email if obj.user else None
