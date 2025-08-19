from rest_framework import serializers
from .models import *


class RecoursesSerializer(serializers.ModelSerializer):
    # get_full_total_sale = serializers.ReadOnlyField()
    # get_full_total_buy = serializers.ReadOnlyField()
    # password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    # password2 = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = Recourses
        fields = "__all__"

class TklfaSerializer(serializers.ModelSerializer):
    # get_full_total_sale = serializers.ReadOnlyField()
    # get_full_total_buy = serializers.ReadOnlyField()
    # password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    # password2 = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = Tklfa
        fields = "__all__"

class AntagDortTsne3Serializer(serializers.ModelSerializer):
    # get_full_total_sale = serializers.ReadOnlyField()
    # get_full_total_buy = serializers.ReadOnlyField()
    # password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    # password2 = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = AntagDortTsne3
        fields = "__all__"


class AntagDortTsne3Serializer(serializers.ModelSerializer):
    # get_full_total_sale = serializers.ReadOnlyField()
    # get_full_total_buy = serializers.ReadOnlyField()
    # password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    # password2 = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = AntagDortTsne3
        fields = "__all__"

class Dof3atDortTsne3Serializer(serializers.ModelSerializer):
    # get_full_total_sale = serializers.ReadOnlyField()
    # get_full_total_buy = serializers.ReadOnlyField()
    # password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    # password2 = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = Dof3atDortTsne3
        fields = "__all__"


class DortTsne3Serializer(serializers.ModelSerializer):
    recoursesItems = serializers.SerializerMethodField(method_name="get_recourses_items", read_only=True)
    tklfaItems = serializers.SerializerMethodField(method_name="get_tklfa_name", read_only=True)
    # x = serializers.ReadOnlyField()
    # password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    # password2 = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = DortTsne3
        fields = "__all__"

    def get_recourses_items(self, obj):
        recourses_items = obj.recourses
        # for i in order_items.values("product"):
        #     pro = Products.objects.get(id=i["product"])
        #     serializer = OrderDetailsSerilizer(pro)
        #
        #
        #     return serializer.data
    #
        serializer = RecoursesSerializer(recourses_items, many=True)
    #
        return serializer.data

    def get_tklfa_items(self, obj):
        tklfa_items = obj.tklfa
        # for i in order_items.values("product"):
        #     pro = Products.objects.get(id=i["product"])
        #     serializer = OrderDetailsSerilizer(pro)
        #
        #
        #     return serializer.data
    #
        serializer = TklfaSerializer(tklfa_items, many=True)
    #
        return serializer.data
