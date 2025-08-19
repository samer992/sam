import requests
from rest_framework import serializers
from .models import *
from rest_framework import status


class MandobEmployeeSerializer(serializers.ModelSerializer):
    mandobproductemp = serializers.SerializerMethodField(method_name="get_user", read_only=True)
    class Meta:
        model = UserEmployee
        fields = "__all__"

    def get_user(self, obj):
        emp_data = obj.mandobproductemp

        serializer = MandobProductsSerializer(emp_data, many=True)
        return serializer.data


class MandobProductsSerializer(serializers.ModelSerializer):
    mandobProductItems = serializers.SerializerMethodField(method_name="get_product_items", read_only=True)
    class Meta:
        model = MandobProducts
        fields = "__all__"

    def get_product_items(self, obj):
        product_items = obj.mandobproductitems

        serializer = MandobPriceBuyProductSerializer(product_items, many=True)
        return serializer.data


class MandobPriceBuyProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = MandobPriceBuyProduct
        fields = "__all__"

# class CatgoryProductTypeSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = CatgoryProductType
#         fields = "__all__"



# class OrderDetailsSerializer(serializers.ModelSerializer):
#     get_full_total_sale = serializers.ReadOnlyField()
#     get_full_total_buy = serializers.ReadOnlyField()
#     # password = serializers.CharField(max_length=100, min_length=6, write_only=True)
#     # password2 = serializers.CharField(max_length=100, min_length=6, write_only=True)
#
#     class Meta:
#         model = OrderDetails
#         fields = "__all__"
#
# class OrderBackDetailsSerializer(serializers.ModelSerializer):
#     get_full_total_sale = serializers.ReadOnlyField()
#     get_full_total_buy = serializers.ReadOnlyField()
#     # password = serializers.CharField(max_length=100, min_length=6, write_only=True)
#     # password2 = serializers.CharField(max_length=100, min_length=6, write_only=True)
#
#     class Meta:
#         model = OrderDetails
#         fields = "__all__"
#
#
# class OrderSerializer(serializers.ModelSerializer):
#     orderItems = serializers.SerializerMethodField(method_name="get_order_items", read_only=True)
#     # ordermanager = serializers.SerializerMethodField(method_name="get_order_name", read_only=True)
#
#
#     class Meta:
#         model = Order
#         fields = "__all__"
#
#     def get_order_items(self, obj):
#         order_items = obj.orderitems.filter(is_finished=False)
#
#         serializer = OrderDetailsSerializer(order_items, many=True)
#
#         return serializer.data
