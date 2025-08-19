
from rest_framework import serializers

from .models import *


class ClientsOrderDetailsSerializer(serializers.ModelSerializer):
    get_full_total_sale = serializers.ReadOnlyField()
    get_full_total_buy = serializers.ReadOnlyField()


    class Meta:
        model = ClientsOrderDetails
        fields = "__all__"


class Dof3atClientsSerializer(serializers.ModelSerializer):
    # get_full_total_sale = serializers.ReadOnlyField()

    class Meta:
        model = Dof3atClients
        fields = "__all__"


class ClientsOrderSerializer(serializers.ModelSerializer):
    clientOrderItems = serializers.SerializerMethodField(method_name="get_clients_items", read_only=True)

    # dof3atOrder = serializers.SerializerMethodField(method_name="get_dof3at_name", read_only=True)

    class Meta:
        model = ClientsOrder
        fields = "__all__"

    def get_clients_items(self, obj):
        clientorder_items = obj.clientorderitems.filter(is_finished=False)

        serializer = ClientsOrderDetailsSerializer(clientorder_items, many=True)

        return serializer.data

    # def get_dof3at_name(self, obj):
    #     dof3at_order = obj.dof3atclientorder
    #
    #     serializer = Dof3atClientsSerializer(dof3at_order, many=True)
    #
    #     return serializer.data


class GroupClientsSerializer(serializers.ModelSerializer):
    clients = serializers.SerializerMethodField(method_name="get_clients", read_only=True)

    class Meta:
        model = GroupClients
        fields = "__all__"

    def get_clients(self, obj):
        clientorder_items = obj.groupClients

        serializer = ClientsSerializer(clientorder_items, many=True)

        return serializer.data


class GroupClientsManagerSerializer(serializers.ModelSerializer):
    clients = serializers.SerializerMethodField(method_name="get_clients", read_only=True)

    class Meta:
        model = GroupClients
        fields = "__all__"

    def get_clients(self, obj):
        clientorder_items = obj.groupclientsmanager

        serializer = ClientsSerializer(clientorder_items, many=True)

        return serializer.data


class ClientsSerializer(serializers.ModelSerializer):
    # get_full_total_sale = serializers.ReadOnlyField()
    order_client = serializers.SerializerMethodField(method_name="get_client_order", read_only=True)
    dof3at_client = serializers.SerializerMethodField(method_name="get_client_dof3at", read_only=True)



    class Meta:
        model = Client
        fields = "__all__"
    def get_client_order(self, obj):
        clientorder = obj.clientorder

        serializer = ClientsOrderSerializer(clientorder, many=True)

        return serializer.data

    def get_client_dof3at(self, obj):
        dof3torder = obj.dof3atclientorders

        serializer = Dof3atClientsSerializer(dof3torder, many=True)

        return serializer.data
