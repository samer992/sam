from rest_framework import serializers


from mandob.serializers import MandobProductsSerializer
from .models import UserEmployee, HadorEmployee, Dof3atEmployee

class HadorEmployeeSerializer(serializers.ModelSerializer):
    # hador_emp = serializers.SerializerMethodField(method_name="get_hadoremp", read_only=True)
    class Meta:
        model = HadorEmployee
        fields = "__all__"


class Dof3atEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dof3atEmployee
        fields = "__all__"


class UserEmployeeSerializer(serializers.ModelSerializer):
    hador_emp = serializers.SerializerMethodField(method_name="get_hadoremp", read_only=True)
    # emp_user = serializers.SerializerMethodField(method_name="get_empuser", read_only=True)

    dof3at_emp = serializers.SerializerMethodField(method_name="get_dof3atemp", read_only=True)
    class Meta:
        model = UserEmployee
        fields = "__all__"

    def get_hadoremp(self, obj):
        hador_emp = obj.hadoremp

        serializer = HadorEmployeeSerializer(hador_emp, many=True)
        return serializer.data

    # def get_empuser(self, obj):
    #     user_emp = obj.empuser
    #
    #     serializer = UserESerializer(user_emp)
    #     return serializer.data


    def get_dof3atemp(self, obj):
        dof3atemp = obj.dof3atemp

        serializer = Dof3atEmployeeSerializer(dof3atemp, many=True)
        return serializer.data

# class UserESerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = "__all__"
#
