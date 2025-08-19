# from rest_framework import serializers
# from .models import Products, UserProfile
# from django import forms
# class ProductsSerilizer(serializers.ModelSerializer):
    # my_sale = serializers.SerializerMethodField(read_only=True)
    # class Meta:
        # fields = "__all__"
    #     fields = ["id", "name", "price", "sale_price", "my_sale"]
    #
    #
    # def get_my_sale(self, obj):
    #     try:
    #         x = obj.x_sale_price()
    #         return x
    #     except:
    #         return None


# class UserProfileSerilizer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = "__all__"