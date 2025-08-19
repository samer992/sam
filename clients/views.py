from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
import datetime
from accounts.models import UserManage, User
from clients.models import GroupClients, Client, ClientsOrder, ClientsOrderDetails, Dof3atClients
from clients.serializers import GroupClientsSerializer, GroupClientsManagerSerializer
from employee.models import UserEmployee
from moduler.models import ModulerUserModel
from shop.models import Products, PriceBuyProduct


# Create your views here.

class AddClient(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_manage = UserManage.objects.get(user=request.user.manageid)
        user_em = User.objects.get(id=request.user.manageid)
        moduler = ModulerUserModel.objects.get(usermanage=user_manage, id=request.data["moduler"])
        moduler_client = ModulerUserModel.objects.get(usermanage=user_manage, name="عملاء")
        employee = UserEmployee.objects.get(usermanager=user_em, time_finshe=False, user=request.user)
        # user_manage = UserManage.objects.get(user=request.user)

        groupclientlist = GroupClients.objects.filter(useremployee=employee, usermanage=user_em)
        #
        print(groupclientlist)
        if groupclientlist:
            print("old client")
            groupclient = GroupClients.objects.get(useremployee=employee, usermanage=user_em)
            client = Client()
            client.usermanage = user_em
            client.first_name = request.data["first_name"]
            client.last_name = request.data["last_name"]
            client.moduler = moduler_client
            client.shop_name = request.data["shop_name"]
            client.description = request.data["description"]
            client.phone = request.data["phone"]
            client.address = request.data["address"]
            client.groupClient = groupclient
            client.save()

        else:
            print("new client")
            groupclients = GroupClients()
            groupclients.usermanage = user_em
            groupclients.moduler = moduler_client
            groupclients.useremployee = employee
            groupclients.description = employee.full_name
            groupclients.type_group_clients = moduler.name
            groupclients.from_moduler = request.data["moduler"]
            groupclients.save()

            client = Client()
            client.usermanage = user_em
            client.first_name = request.data["first_name"]
            client.last_name = request.data["last_name"]
            client.moduler = moduler_client
            client.shop_name = request.data["shop_name"]
            client.description = request.data["description"]
            client.phone = request.data["phone"]
            client.address = request.data["address"]
            client.groupClient = groupclients
            client.save()
        return Response("تم اضافه عميل جديد", status=status.HTTP_201_CREATED)



    def get(self, request):
        user = request.user
        if user.is_authenticated:
            use = request.user.manageid
            if user.manager:
                groupclients = GroupClients.objects.filter(usermanage=user)
                print(groupclients)
                serializer = GroupClientsSerializer(instance=groupclients, many=True)
                print(serializer.data)
                return Response({"groupclients": serializer.data}, status=status.HTTP_200_OK)
            else:
                user_man = User.objects.get(id=use)
                employee = UserEmployee.objects.get(usermanager=user_man, time_finshe=False, user=request.user)
                # print(request.GET["from_moduler"]+"xxxxxxxxxxxxxxxxxxxxxxxxx")

            # pro = MandobProducts.objects.filter(usermanage=user_man, moduler=request.GET["moduler"])
                if not GroupClients.objects.filter(usermanage=user_man, useremployee=employee, from_moduler=request.GET["from_moduler"]).exists():
                    print("nooooooooooooooooo")
                    return Response("لم يتم اضافه عملاء", status=status.HTTP_400_BAD_REQUEST)

                else:
                    groupclients = GroupClients.objects.get(usermanage=user_man, useremployee=employee,
                                                            from_moduler=request.GET["from_moduler"])

                    serializer = GroupClientsSerializer(instance=groupclients)
                    print(serializer.data)
                    return Response({"clients": serializer.data["clients"]}, status=status.HTTP_200_OK)

def clientOrder(req, man, use, emp_id, closeD, mang):
    useremp = UserEmployee.objects.get(user=use, usermanager=man, time_finshe=False)
    client = Client.objects.get(id=emp_id)
    ###################المنتجات مكان واحد بس قسمهم اظبط product
    for order_request in req:



        print(order_request["moduler"])
        print(mang)
        moduler_user = ModulerUserModel.objects.get(usermanage=mang, id=order_request["moduler"])
        order_request_barcode = order_request["barcode_id"]
        order_request_payment = float(order_request["Payment"])
        order_request_orderItems = order_request["orderItems"]
        # print(order_request_barcode)
        # print(order_request_payment)
        # print("orders_items_request")
        order_total = []


        for request_orderItem in order_request_orderItems:
            order_request_orderItem_price = float(request_orderItem["price"])
            order_request_orderItem_quantity = float(request_orderItem["quantity"])
            order_total.append(order_request_orderItem_quantity*order_request_orderItem_price)

        new_order = ClientsOrder()
        new_order.user = use
        new_order.usermanage = man
        new_order.order_date = datetime.datetime.now()
        new_order.is_finished = True
        new_order.barcode_id = order_request_barcode
        new_order.client = client
        new_order.useremployee = useremp
        total = sum(order_total)
        stay = order_request_payment - float(sum(order_total))
        new_order.total = total
        new_order.stay = stay
        new_order.moduler = moduler_user
        new_order.Payment = order_request_payment
        print(f"xxxxxxTOTALxxxxxxclliiiieeeeeeeeennnnnnnttttttt: {total}")
        print(f"xxxxxxSTAYxxxxxxxcllllliientttttt: {stay}")




        for order_request_orderItem in order_request_orderItems:
            order_request_orderItem_barcode = order_request_orderItem["product"]
            order_request_orderItem_price = float(order_request_orderItem["price"])
            order_request_orderItem_quantity = float(order_request_orderItem["quantity"])
            # order_total.append(order_request_orderItem_quantity*order_request_orderItem_price)
            # print(order_request_orderItem_barcode)
            # print(order_request_orderItem_price)

            product = Products.objects.get(barcode_id=order_request_orderItem_barcode)

            Price_Buy_Products = PriceBuyProduct.objects.all().filter(product=product, is_finished=False)
            # print("Price_Buy_Products################################")
            total_quantity_price_Buy = 0
            for price_Buy_Product in Price_Buy_Products:
                total_quantity_price_Buy += price_Buy_Product.quantity

            if order_request_orderItem_quantity <= total_quantity_price_Buy:

                print(f"order_request_orderItem_quantity ==> {order_request_orderItem_quantity}")
                print(f"total_quantity_price_Buy_Product ==> {total_quantity_price_Buy}")
                if order_request_orderItem_quantity != 0:
                    new_order.save()
                    for price_Buy_Product_InQty in Price_Buy_Products:
                        price_Buy_Product_qty = float(price_Buy_Product_InQty.quantity)
                        print(price_Buy_Product_InQty.quantity)


                        if order_request_orderItem_quantity <= price_Buy_Product_InQty.quantity:
                            price_Buy_Product_qty -= order_request_orderItem_quantity
                            price_Buy_Product_InQty.quantity = price_Buy_Product_qty
                            price_Buy_Product_InQty.save()
                            quantity_to_order_details = order_request_orderItem_quantity
                            order_request_orderItem_quantity = 0
                            print(f"<= {price_Buy_Product_qty}")
                        else:
                            order_request_orderItem_quantity -= price_Buy_Product_qty
                            print(f"> {order_request_orderItem_quantity}")
                            price_Buy_Product_InQty.quantity = 0
                            price_Buy_Product_InQty.is_finished = True
                            price_Buy_Product_InQty.save()
                            quantity_to_order_details = price_Buy_Product_qty

                        order_details = ClientsOrderDetails.objects.create(
                            # product=product,
                            order=new_order,
                            name=product.name,
                            img=product.product_picture,
                            price=order_request_orderItem_price,
                            quantity=quantity_to_order_details,
                            price_buy=price_Buy_Product_InQty.price_buy,
                            dec_product=product.description,
                            type_quantity=product.type_quantity,
                            barcode_id=product.barcode_id
                        )
                        order_details.save()

                else:
                    return Response(f" {product}ادخل كميه",
                                    status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(f"الكميه {product} غير كافيه باقى {total_quantity_price_Buy}", status=status.HTTP_400_BAD_REQUEST)


        print("saaaaaaaaaaam")
        print(order_request["is_agel"])
        # من اجل الدفعات
        add_dof3a = Dof3atClients()
        add_dof3a.client = client
        add_dof3a.useremployee = useremp
        add_dof3a.description = "من الفاتوره"
        if order_request["is_agel"]:
            print("yes")
            print(order_request_payment)

            add_dof3a.dof3a = order_request_payment

        else:
            print("nooooooooooo")
            print(sum(order_total))
            add_dof3a.dof3a = sum(order_total)
        add_dof3a.save()
        return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def Dof3at(request):
    user_em = User.objects.get(id=request.user.manageid)
    useremp = UserEmployee.objects.get(user=request.user, usermanager=user_em, time_finshe=False)
    client = Client.objects.get(id=request.data["idClient"])
    print(request.data["idClient"])
    print(request.data["dof3a"])
    add_dof3a = Dof3atClients()
    add_dof3a.client = client
    add_dof3a.useremployee = useremp
    add_dof3a.description = "من العميل"
    add_dof3a.dof3a = request.data["dof3a"]
    add_dof3a.save()

    return Response("تم اضافه الدفعه الجديده", status=status.HTTP_201_CREATED)