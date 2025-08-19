
from barcode.writer import ImageWriter
from io import BytesIO
import barcode
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.core.files import File
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.models import *
from accounts.serializers import ProfileSerializer
from moduler.models import ModulerUserModel
from .serializers import ProductsSerializer, CatgoryProductTypeSerializer, OrderSerializer, OrderBackDetailsSerializer
from rest_framework.response import Response
from .models import Productsmakhzen, PriceBuyProductmakhzen, CatgoryProductTypemakhzen, Ordermakhzen, OrderDetailsmakhzen, ClosedEmpmakhzen, ClosedDaymakhzen, OrderBackDetailsmakhzen
from rest_framework.parsers import MultiPartParser, FormParser
import random
# Create your views here.
################### ==> Products <== ###################
class productsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductsSerializer
    parsers_classes = [MultiPartParser, FormParser]
    print("xxxxxxxxxxxxxxxxxxxxxxxxxx")

    # @swagger_auto_schema(operation_summary="Get all Orders")
    def post(self, request, format=None):

        if request.user.manager:
            product_data = request.data
            print(request.data["barcode_id"])
            if product_data["barcode_id"]:
                print("ok")
            else:
                contary_code = 6
                segl_tgary = 123456
                id_pro = random.randint(11111, 99999)
                product_data["barcode_id"] = number = f"{contary_code}{segl_tgary}{id_pro}"
                print('not ok')
                print(number)
            # print(request.data["id_pro"])
            products = Productsmakhzen.objects.all().filter(user=request.user)
            # print(len(products))
            userman = UserManage.objects.get(user=request.user)
            num_products = ModulerUserModel.objects.get(usermanage=userman, id=product_data["moduler"])
            if len(products) < num_products.num_products:
                produc = Productsmakhzen.objects.all().filter(user=request.user, barcode_id=product_data["barcode_id"])
                if produc:
                    print(produc)
                    old_product = Productsmakhzen.objects.get(user=request.user, id=produc[0].id, barcode_id=product_data["barcode_id"])
                    price_BuyProduct = PriceBuyProductmakhzen.objects.all().filter(product=old_product, price_buy=product_data["price_buy"])
                    total_quantity = float(old_product.total_quantity) + float(product_data["quantity"])
                    if price_BuyProduct:
                        old_price_BuyProduct = PriceBuyProductmakhzen.objects.get(product=old_product, price_buy=product_data["price_buy"])
                        quantity = float(old_price_BuyProduct.quantity) + float(product_data["quantity"])
                        print(old_product)
                        old_price_BuyProduct.quantity = quantity
                        old_price_BuyProduct.quantity_total = quantity
                        old_price_BuyProduct.total_buy = float(quantity)*float(product_data["price_buy"])
                        old_price_BuyProduct.save()
                        print(price_BuyProduct)
                        print("فيه سعر منتج قديم")
                    else:
                        priceBuyProduct = PriceBuyProductmakhzen.objects.create(
                            product=old_product,
                            quantity=product_data["quantity"],
                            quantity_total=product_data["quantity"],
                            price_buy=product_data["price_buy"],
                            total_buy=float(product_data["quantity"])*float(product_data["price_buy"]),
                        )
                        priceBuyProduct.save()
                        print(" سعر منتج جديد")

                    old_product.total_quantity = total_quantity
                    old_product.total_sale = float(product_data["price_sale"])*total_quantity
                    old_product.price_sale = product_data["price_sale"]
                    old_product.save()

                    print("فيه منتج قديم")

                else:
                    print("منتج جديد")
                    # print(os.getcwd())
                    # print(settings.MEDIA_ROOT)

                    options = {
                        'format': 'PNG',
                        'font_size': 20,
                        'text_distance': 2.0,
                    }
                    xxx = barcode.get_barcode_class("code128")
                    xcv = xxx(product_data["barcode_id"], writer=ImageWriter().set_options(options=options))
                    buffer = BytesIO()
                    xcv.write(buffer)
                    # print(File(buffer).read)
                    path_fol = settings.MEDIA_ROOT + "\images\\"

                    xcv.save(path_fol+product_data['name'], File(buffer))
                    print(product_data["product_picture"])

                    pro = Productsmakhzen()
                    pro.user = request.user
                    pro.name = product_data["name"]
                    pro.description = product_data["description"]
                    pro.price_sale = product_data["price_sale"]
                    pro.barcode_id = xcv #str(my_code)
                    pro.total_quantity = product_data["quantity"]
                    pro.product_picture = product_data["product_picture"]
                    pro.is_active = product_data["is_active"]
                    pro.barcode = f"images/{product_data['name']}.svg"
                    pro.total_sale = float(product_data["price_sale"])*float(product_data["quantity"])
                    pro.type_id = product_data["type_id"]
                    pro.type_quantity = product_data["type_quantity"]
                    pro.moduler = num_products

                    pro.save()
                    priceBuyProduct = PriceBuyProductmakhzen.objects.create(
                        product=pro,
                        quantity=product_data["quantity"],
                        quantity_total=product_data["quantity"],
                        price_buy=float(product_data["price_buy"]),
                        total_buy=float(product_data["quantity"]) * float(product_data["price_buy"]),
                    )
                    priceBuyProduct.save()
                return Response({
                    'data': "product",
                    'message': f"تم اضافه {request.data['name']} بنجاح",
                    "status": "Your account regestrathion susccessfuly"
                }, status=status.HTTP_201_CREATED)
            else:
                # print(len(products))
                return Response({
                    'data': "المنتجات خلصت زود منتجات",
                    'message': f"لم يتم اضافه {request.data['name']} ",
                }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"data": "انته مش مدير"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        if user.manager:
            pro = Productsmakhzen.objects.filter(user=request.user)
        else:
            pro = Productsmakhzen.objects.filter(user=request.user.manageid)

        # product_data = request.data

        serializer = self.serializer_class(instance=pro, many=True)
        # if serializer.is_valid(raise_exception=True):
            # serializer.save()
        product = serializer.data
        # print(product)

        return Response({"data": product}, status=status.HTTP_200_OK)
        # return Response({product})



class CatgoryProductTypeViw(GenericAPIView):
    print("saaaaaaaaaaammm")
    permission_classes = [IsAuthenticated]
    serializer_class = CatgoryProductTypeSerializer

    def post(self, request):
        if request.user.is_authenticated:
            catgoryproduct = CatgoryProductTypemakhzen.objects.create(
            user=request.user,
            name=request.data["name"]
            )
            catgoryproduct.save()

        print("request poooooooooooooost")
        return Response({"data": "تم الأضافه بنجاح"}, status=status.HTTP_201_CREATED)

    def get(self, request):
        print(request.user)
        user = request.user
        if user.manager:
            pass
            # print(user)
        else:
            # print(user)
            user = user.manageid
        catgory = CatgoryProductTypemakhzen.objects.filter(user=user)

        serializer = self.serializer_class(instance=catgory, many=True)

        catgoryproduct = serializer.data
        print("request geeeeeeeeeeeeeeeeet")

        return Response({"data": catgoryproduct}, status=status.HTTP_200_OK)

    def delete(self, request):
        print(request.GET["id"])
        # print(id)
        catgoryProductType = get_object_or_404(CatgoryProductTypemakhzen, id=request.GET["id"])
        # print(product_2.user)
        # product = get_object_or_404(User, id=product_2.user_id)
        # print(product)

        #
        # if product.user != request.user:
        #     return Response({"error": "Sorry you can not update this product"}
        #                     , status=status.HTTP_403_FORBIDDEN)
        #
        catgoryProductType.delete()
        # product_2.delete()
        return Response({"details": "Delete action is done"}, status=status.HTTP_200_OK)


#################### ==> Orders <== ####################
# from rest_framework.authtoken.models import Token
class Cart(GenericAPIView):
    permission_classes = [IsAuthenticated]
    ########################post tb3on al cart#####################
    # [
    #     {
    #         "barcode_id": "111111111111",
    #         "Payment": "100",
    #         "product": [
    #             {
    #                 "quantity": 3,
    #                 "barcode_pro": "620240432617"
    #             },
    #             {
    #                 "quantity": 50,
    #                 "barcode_pro": "620240462955"
    #             }
    #         ]
    #
    #     }
    # ]
    def post(self, request):
        user = request.user
        # print(user+"rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        # print(request.data)
        if user.emp:
            user_man = User.objects.get(id=user.manageid)
            # print("its emp")
        else:
            user_man = request.user
        # print(user_man)

        if not ClosedDaymakhzen.objects.filter(usermanage=user_man, is_finished=False).exists():
            closeDay = ClosedDaymakhzen()
            closeDay.usermanage = user_man
            closeDay.save()

        else:
            closeDay = ClosedDaymakhzen.objects.get(usermanage=user_man, is_finished=False)


        if not ClosedEmpmakhzen.objects.filter(user=user, is_finished=False).exists():
            print(closeDay)
            closedEmp = ClosedEmpmakhzen()
            closedEmp.usermanage = user_man
            closedEmp.user = request.user
            closedEmp.emp_name = request.user.get_full_name
            closedEmp.close_day = closeDay
            closedEmp.save()
            # print(closedEmp)
            print("wwwwwwwwwwwwwwwwwwwwwwwwwww")
        else:
            closedEmp = ClosedEmpmakhzen.objects.get(user=user, is_finished=False)
            # print(closeDay)
            # print(closedEmp)
            print("nnnnnnnnnnnnnnnnnnnnnnnn")
        for order_request in request.data:
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

            new_order = Ordermakhzen()
            new_order.user = request.user
            new_order.usermanage = user_man
            new_order.order_date = datetime.datetime.now()
            new_order.is_finished = True
            new_order.barcode_id = order_request_barcode
            new_order.close_emp = closedEmp
            new_order.close_day = closeDay
            total = sum(order_total)
            stay = order_request_payment - float(sum(order_total))
            new_order.total = total
            new_order.stay = stay
            new_order.Payment = order_request_payment
            print(f"xxxxxxTOTALxxxxxx: {total}")
            print(f"xxxxxxSTAYxxxxxxx: {stay}")
            new_order.save()



            for order_request_orderItem in order_request_orderItems:
                order_request_orderItem_barcode = order_request_orderItem["product"]
                order_request_orderItem_price = float(order_request_orderItem["price"])
                order_request_orderItem_quantity = float(order_request_orderItem["quantity"])
                order_total.append(order_request_orderItem_quantity*order_request_orderItem_price)
                # print(order_request_orderItem_barcode)
                # print(order_request_orderItem_price)

                product = Productsmakhzen.objects.get(barcode_id=order_request_orderItem_barcode)
                Price_Buy_Products = PriceBuyProductmakhzen.objects.all().filter(product=product, is_finished=False)
                # print("Price_Buy_Products################################")
                total_quantity_price_Buy = 0
                for price_Buy_Product in Price_Buy_Products:
                    total_quantity_price_Buy += price_Buy_Product.quantity

                if order_request_orderItem_quantity <= total_quantity_price_Buy:

                    print(f"order_request_orderItem_quantity ==> {order_request_orderItem_quantity}")
                    print(f"total_quantity_price_Buy_Product ==> {total_quantity_price_Buy}")
                    for price_Buy_Product_InQty in Price_Buy_Products:
                        price_Buy_Product_qty = float(price_Buy_Product_InQty.quantity)
                        print(price_Buy_Product_InQty.quantity)
                        if order_request_orderItem_quantity != 0:
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
                            order_details = OrderDetailsmakhzen.objects.create(
                                product=product,
                                order=new_order,
                                name=product.name,
                                img=product.product_picture,
                                price=order_request_orderItem_price,
                                quantity=quantity_to_order_details,
                                price_buy=price_Buy_Product_InQty.price_buy,
                                dec_product=product.description,
                                type_quantity=product.type_quantity,
                            )
                            order_details.save()


                    print("كافيه الكميه كافيه")
                else:
                    print("غير الكميه غير كافيه غير")


        return Response("تمت عمليه الدفع", status=status.HTTP_201_CREATED)

##################################################################################
    def get(self, request):
        user = request.user
        print(user)
        print(request.GET["order_barcode"])

        if user.emp:
            user_man = User.objects.get(id=user.manageid)
            print("its emp")
        else:
            user_man = request.user
        print(user_man)


        ordr = Ordermakhzen.objects.filter(barcode_id=request.GET["order_barcode"])
        if ordr:
            order = Ordermakhzen.objects.get(barcode_id=request.GET["order_barcode"])
            user_order = User.objects.get(id=order.user_id)

            serializer = OrderSerializer(instance=order)

            return Response({"order": serializer.data, "user_order": user_order.get_full_name}, status=status.HTTP_200_OK)
        else:
            return Response("لا يوجد فاتوره", status=status.HTTP_404_NOT_FOUND)






@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def orderxx(request):
    user = request.user
    if user.emp:
        user_man = User.objects.get(id=user.manageid)
        # print("its emp")
    else:
        user_man = request.user
    print(user)
    orders = Ordermakhzen.objects.filter(usermanage=user_man, is_finished=True)
    name_order = []
    for order in orders:
        # print(order.order_date)

        user_order = User.objects.get(id=order.user_id)
        name_order.append(user_order.get_full_name)
        # print(user_order.get_full_name)
    serializer = OrderSerializer(instance=orders, many=True)


    # print(serializer.data["ordermanager"])
    return Response({"data": serializer.data, "user_order": name_order}, status=status.HTTP_200_OK)


@api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def backorder(request):
    user = request.user
    print(request.data["id_order"])
    print(request.data["orderItemsListEdit"])# امان ميرحوش فاضى يعمل error
    if user.emp:
        user_man = User.objects.get(id=user.manageid)
        # print("its emp")
    else:
        user_man = request.user
    orders = Ordermakhzen.objects.filter(usermanage=user_man, id=request.data["id_order"])
    # print(orders)
    if orders:
        # orderItems_id = request.data["orderItemsListEdit"][0]["orderItems_id"]
        # orderItems_quantity = request.data["orderItemsListEdit"][0]["quantity"]
        for i in request.data["orderItemsListEdit"]:
            print(i["orderItems_id"])

            order_detl = OrderDetailsmakhzen.objects.get(id=i["orderItems_id"], order=request.data["id_order"])
            xx = float(order_detl.quantity) - i["quantity"]
            print(xx)
            order_detl.quantity = xx
            if xx == 0:
                order_detl.is_finished = True


            order_detl.save()
        # print(order_detl)
            order = orders[0]
            orderbackdetails = OrderBackDetailsmakhzen.objects.create(
                product=order_detl.product,
                order=order,
                name=order_detl.name,
                img=order_detl.img,
                price=order_detl.price,
                quantity=i["quantity"],
                price_buy=order_detl.price_buy,
                dec_product=order_detl.dec_product,
                type_quantity=order_detl.type_quantity,
                usermanage=order.usermanage,
            )
            orderbackdetails.save()
        # print(orderbackdetails)
        orderdetails = OrderDetailsmakhzen.objects.filter(order=order, is_finished=False)
        print(order)
        print(orderdetails)
        total_order = 0
        if orderdetails:
            for orderdetail in orderdetails:
                total_order += orderdetail.quantity*orderdetail.price
            print(total_order)
            order.total = total_order

            order.save()
        else:
            order.delete()

    else:
        print("noooooooooooo order hnaaaaaaaaaaaa")

    return Response({"data"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def backproduct(request):
    user = request.user
    if user.emp:
        user_man = User.objects.get(id=user.manageid)
        # print("its emp")
    else:
        user_man = request.user
    print(user)
    orders = OrderBackDetailsmakhzen.objects.filter(usermanage=user_man, is_finished=False)

    serializer = OrderBackDetailsSerializer(instance=orders, many=True)


    # print(serializer.data["ordermanager"])
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def closebackorder(request):
    print(request.data["id"])
    orderBackDetails = OrderBackDetailsmakhzen.objects.get(usermanage=request.user, is_finished=False, id=request.data["id"])
    orderBackDetails.is_finished = True
    orderBackDetails.save()
    return Response({"data": "تمت العمليه بنجاح"}, status=status.HTTP_200_OK)


