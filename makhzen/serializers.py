import requests
from rest_framework import serializers
from .models import *
from rest_framework import status


class ProductsSerializer(serializers.ModelSerializer):
    productItems = serializers.SerializerMethodField(method_name="get_product_items", read_only=True)
    class Meta:
        model = Productsmakhzen
        fields = "__all__"

    def get_product_items(self, obj):
        product_items = obj.productitems.all()

        serializer = PriceBuyProductSerializer(product_items, many=True)
        return serializer.data


class PriceBuyProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = PriceBuyProductmakhzen
        fields = "__all__"

class CatgoryProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatgoryProductTypemakhzen
        fields = "__all__"



class OrderDetailsSerializer(serializers.ModelSerializer):
    get_full_total_sale = serializers.ReadOnlyField()
    get_full_total_buy = serializers.ReadOnlyField()
    # password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    # password2 = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = OrderDetailsmakhzen
        fields = "__all__"

class OrderBackDetailsSerializer(serializers.ModelSerializer):
    get_full_total_sale = serializers.ReadOnlyField()
    get_full_total_buy = serializers.ReadOnlyField()
    # password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    # password2 = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = OrderBackDetailsmakhzen
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(method_name="get_order_items", read_only=True)
    # ordermanager = serializers.SerializerMethodField(method_name="get_order_name", read_only=True)
    # x = serializers.ReadOnlyField()
    # password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    # password2 = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = Ordermakhzen
        fields = "__all__"

    def get_order_items(self, obj):
        order_items = obj.orderitems.filter(is_finished=False)
        # for i in order_items.values("product"):
        #     pro = Products.objects.get(id=i["product"])
        #     serializer = OrderDetailsSerilizer(pro)
        #
        #
        #     return serializer.data
    #
        serializer = OrderDetailsSerializer(order_items, many=True)
    #
        return serializer.data
