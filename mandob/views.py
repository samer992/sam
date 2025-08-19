import datetime

from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User, UserManage
from clients.views import clientOrder
from employee.models import UserEmployee
from makhzen.models import Productsmakhzen
from mandob.models import MandobProducts, MandobPriceBuyProduct, MandobClosedDay, MandobOrder, MandobOrderDetails
from mandob.serializers import MandobProductsSerializer, MandobEmployeeSerializer
from moduler.models import ModulerUserModel
from shop.models import Products
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Create your views here.
class MandobProductsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MandobProductsSerializer
    parsers_classes = [MultiPartParser, FormParser]


    # @swagger_auto_schema(operation_summary="Get all Orders")
    def post(self, request, format=None):

        if request.user.manager:
            use = request.user.manageid
            user_man = User.objects.get(id=use)
            product_data = request.data
            print(request.data["barcode_id"])
            print(product_data["moduler"])
            # if product_data["barcode_id"]:
            #     print("ok")
            # else:
            #     contary_code = 6
            #     segl_tgary = 123456
            #     id_pro = random.randint(11111, 99999)
            #     product_data["barcode_id"] = number = f"{contary_code}{segl_tgary}{id_pro}"
            #     print('not ok')
            #     print(number)
            # print(request.data["id_pro"])
            userman = UserManage.objects.get(user=user_man)
            useremp_mandob = UserEmployee.objects.get(id=product_data["emp_id"])
            moduler_mandob = ModulerUserModel.objects.get(usermanage=userman, name="مندوب")
            moduler = ModulerUserModel.objects.get(usermanage=userman, id=product_data["moduler"])
            if moduler.name == "محل":
                product = Products.objects.get(usermanage=user_man, moduler=moduler, barcode_id=request.data["barcode_id"])
            if moduler.name == "مخزن":
                product = Productsmakhzen.objects.filter(usermanage=user_man, moduler=moduler)
            print(moduler)
            print(product)
            print(useremp_mandob)
            print(product_data["quantity"])
            print(moduler_mandob)

            # if len(products) < moduler.num_products:
            produc = MandobProducts.objects.all().filter(usermanage=user_man, barcode_id=product_data["barcode_id"], moduler=moduler, useremployee=useremp_mandob)
            if produc:
                print(produc)
                old_product = MandobProducts.objects.get(usermanage=user_man, id=produc[0].id, barcode_id=product_data["barcode_id"], moduler=moduler)
                price_BuyProduct = MandobPriceBuyProduct.objects.all().filter(product=old_product, price_buy=product_data["price_buy"])
                total_quantity = float(old_product.total_quantity) + float(product_data["quantity"])
                if price_BuyProduct:
                    old_price_BuyProduct = MandobPriceBuyProduct.objects.get(product=old_product, price_buy=product_data["price_buy"])
                    quantity = float(old_price_BuyProduct.quantity) + float(product_data["quantity"])
                    print(old_product)
                    old_price_BuyProduct.quantity = quantity
                    old_price_BuyProduct.quantity_total = quantity
                    old_price_BuyProduct.total_buy = float(quantity)*float(product_data["price_buy"])
                    old_price_BuyProduct.is_finished = False
                    old_price_BuyProduct.save()
                    print(price_BuyProduct)
                    print("فيه سعر منتج قديم")
                else:
                    priceBuyProduct = MandobPriceBuyProduct.objects.create(
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

                # options = {
                #     'format': 'PNG',
                #     'font_size': 20,
                #     'text_distance': 2.0,
                # }
                # # xxx = barcode.get_barcode_class("code128")
                # # xcv = xxx(product_data["barcode_id"], writer=ImageWriter().set_options(options=options))
                # # buffer = BytesIO()
                # # xcv.write(buffer)
                # # # print(File(buffer).read)
                # # path_fol = settings.MEDIA_ROOT + "\images\\"
                # #
                # # xcv.save(path_fol+product_data['name'], File(buffer))
                # print(product_data["product_picture"])
                #
                pro = MandobProducts()
                pro.user = request.user
                pro.name = product.name
                pro.useremployee = useremp_mandob
                pro.description = product.description
                pro.price_sale = product.price_sale
                pro.barcode_id = product.barcode_id #str(my_code)
                pro.total_quantity = product_data["quantity"]
                pro.product_picture = product.product_picture
                pro.is_active = product_data["is_active"]
                # pro.barcode = f"images/{product_data['name']}.svg"
                pro.total_sale = float(product.price_sale)*float(product_data["quantity"])
                pro.type_id = product.type_id
                pro.type_quantity = product.type_quantity
                pro.moduler = moduler
                pro.usermanage = product.usermanage
                #
                pro.save()
                for i in product_data["product_details"]:
                    priceBuyProduct = MandobPriceBuyProduct.objects.create(
                        product=pro,
                        quantity=i["quantity"],
                        quantity_total=i["quantity"],
                        price_buy=float(i["price_buy"]),
                        total_buy=float(i["quantity"]) * float(i["price_buy"]),
                    )
                    priceBuyProduct.save()

                return Response({
                    'data': "product",
                    'message': f"تم اضافه {product} بنجاح",
                    "status": "Your account regestrathion susccessfuly"
                }, status=status.HTTP_201_CREATED)
            # else:
                # print(len(products))
            return Response({
                    'data': "المنتجات خلصت زود منتجات",
                    'message': f"لم يتم اضافه {useremp_mandob} ",
                }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"data": "انته مش مدير"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            use = request.user.manageid
            user_man = User.objects.get(id=use)
            userman = UserManage.objects.get(user=user_man)
            useremp = UserEmployee.objects.get(usermanager=user_man, user=request.user)
            moduler_mandob = ModulerUserModel.objects.get(usermanage=userman, id=request.GET["moduler"])
        pro = MandobProducts.objects.filter(usermanage=user_man, moduler=moduler_mandob, useremployee=useremp)

        serializer = self.serializer_class(instance=pro, many=True)

        product = serializer.data
        print(product)

        return Response({"mandobproductemp": product}, status=status.HTTP_200_OK)






def mntgat_mandob(barcode_id, user_man, moduler, emp_id,user,product_details,to_quantity):
        userman = UserManage.objects.get(user=user_man)
        useremp_mandob = UserEmployee.objects.get(id=emp_id)
        moduler_mandob = ModulerUserModel.objects.get(usermanage=userman, name="مندوب")
        # moduler = ModulerUserModel.objects.get(usermanage=userman, id=product_data["moduler"])
        if moduler.name == "محل":
            product = Products.objects.get(usermanage=user_man, moduler=moduler, barcode_id=barcode_id)
        if moduler.name == "مخزن":
            product = Productsmakhzen.objects.filter(usermanage=user_man, moduler=moduler)


        # if len(products) < moduler.num_products:
        produc = MandobProducts.objects.all().filter(usermanage=user_man, barcode_id=barcode_id, moduler=moduler, useremployee=useremp_mandob)
        if produc:
            print(produc)
            old_product = MandobProducts.objects.get(usermanage=user_man, id=produc[0].id, moduler=moduler)
            for x in product_details:
                price_BuyProduct = MandobPriceBuyProduct.objects.all().filter(product=old_product, price_buy=x["price_buy"])
                total_quantity = float(old_product.total_quantity) + float(x["quantity"])
                if price_BuyProduct:
                    old_price_BuyProduct = MandobPriceBuyProduct.objects.get(product=old_product, price_buy=x["price_buy"])
                    quantity = float(old_price_BuyProduct.quantity) + float(x["quantity"])
                    print(old_product)
                    old_price_BuyProduct.quantity = quantity
                    old_price_BuyProduct.quantity_total = quantity
                    old_price_BuyProduct.total_buy = float(quantity)*float(x["price_buy"])
                    old_price_BuyProduct.is_finished = False
                    old_price_BuyProduct.save()
                    print(price_BuyProduct)
                    print("فيه سعر منتج قديم")
                else:
                    priceBuyProduct = MandobPriceBuyProduct.objects.create(
                        product=old_product,
                        quantity=x["quantity"],
                        quantity_total=x["quantity"],
                        price_buy=x["price_buy"],
                        total_buy=float(x["quantity"])*float(x["price_buy"]),
                    )
                    priceBuyProduct.save()
                    print(" سعر منتج جديد")

                old_product.total_quantity = total_quantity
                old_product.total_sale = float(old_product.price_sale)*total_quantity
                old_product.price_sale = old_product.price_sale
                old_product.save()

                print("فيه منتج قديم")

        else:
            print("منتج جديد")
            # print(os.getcwd())
            # print(settings.MEDIA_ROOT)

            # options = {
            #     'format': 'PNG',
            #     'font_size': 20,
            #     'text_distance': 2.0,
            # }
            # # xxx = barcode.get_barcode_class("code128")
            # # xcv = xxx(product_data["barcode_id"], writer=ImageWriter().set_options(options=options))
            # # buffer = BytesIO()
            # # xcv.write(buffer)
            # # # print(File(buffer).read)
            # # path_fol = settings.MEDIA_ROOT + "\images\\"
            # #
            # # xcv.save(path_fol+product_data['name'], File(buffer))
            # print(product_data["product_picture"])
            #
            pro = MandobProducts()
            pro.user = user
            pro.name = product.name
            pro.useremployee = useremp_mandob
            pro.description = product.description
            pro.price_sale = product.price_sale
            pro.barcode_id = product.barcode_id #str(my_code)
            pro.total_quantity = to_quantity
            pro.product_picture = product.product_picture
            pro.is_active = True
            # pro.barcode = f"images/{product_data['name']}.svg"
            pro.total_sale = float(product.price_sale)*float(to_quantity)
            pro.type_id = product.type_id
            pro.type_quantity = product.type_quantity
            pro.moduler = moduler_mandob
            pro.usermanage = product.usermanage
            #
            pro.save()
            for i in product_details:
                priceBuyProduct = MandobPriceBuyProduct.objects.create(
                    product=pro,
                    quantity=i["quantity"],
                    quantity_total=i["quantity"],
                    price_buy=float(i["price_buy"]),
                    total_buy=float(i["quantity"]) * float(i["price_buy"]),
                )
                priceBuyProduct.save()

            return Response({
                'data': "product",
                'message': f"تم اضافه {product} بنجاح",
                "status": "Your account regestrathion susccessfuly"
            }, status=status.HTTP_201_CREATED)
        # else:
            # print(len(products))
        # return Response({
        #         'data': "المنتجات خلصت زود منتجات",
        #         'message': f"لم يتم اضافه {useremp_mandob} ",
        #     }, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_mandob_products(request):
    user = request.user
    if user.is_authenticated:
        use = request.user.manageid
        user_m = User.objects.get(id=use)

    employee = UserEmployee.objects.all().filter(usermanager=user_m, time_finshe=False, type_work="mandob")
    serializer = MandobEmployeeSerializer(instance=employee, many=True)

    return Response({"productsMandobs": serializer.data}, status=status.HTTP_200_OK)




class Cart(GenericAPIView):
    permission_classes = [IsAuthenticated]
    ########################post tb3on al cart#####################
    # [
    #     {
    #         "barcode_id": "111111111111",
    #         "Payment": "100",
    #         "moduler": 1,
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
    def checkOrder(self, req, man, use, closeD, mang):
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

            new_order = MandobOrder()
            new_order.user = use
            new_order.usermanage = man
            new_order.order_date = datetime.datetime.now()
            new_order.is_finished = True
            new_order.barcode_id = order_request_barcode

            new_order.close_day = closeD
            total = sum(order_total)
            stay = order_request_payment - float(sum(order_total))
            new_order.total = total
            new_order.stay = stay
            new_order.moduler = moduler_user
            new_order.Payment = order_request_payment
            print(f"xxxxxxTOTALxxxxxx: {total}")
            print(f"xxxxxxSTAYxxxxxxx: {stay}")




            for order_request_orderItem in order_request_orderItems:
                order_request_orderItem_barcode = order_request_orderItem["product"]
                order_request_orderItem_price = float(order_request_orderItem["price"])
                order_request_orderItem_quantity = float(order_request_orderItem["quantity"])
                order_total.append(order_request_orderItem_quantity*order_request_orderItem_price)
                # print(order_request_orderItem_barcode)
                # print(order_request_orderItem_price)

                product = MandobProducts.objects.get(barcode_id=order_request_orderItem_barcode)

                Price_Buy_Products = MandobPriceBuyProduct.objects.all().filter(product=product, is_finished=False)
                # print("Price_Buy_Products################################")
                total_quantity_price_Buy = 0
                for price_Buy_Product in Price_Buy_Products:
                    total_quantity_price_Buy += price_Buy_Product.quantity

                if order_request_orderItem_quantity <= total_quantity_price_Buy:

                    print(f"order_request_orderItem_quantity ==> {order_request_orderItem_quantity}")
                    print(f"total_quantity_price_Buy_Product ==> {total_quantity_price_Buy}")
                    if order_request_orderItem_quantity != 0:
                        # new_order.save()
                        for price_Buy_Product_InQty in Price_Buy_Products:
                            price_Buy_Product_qty = float(price_Buy_Product_InQty.quantity)
                            print(price_Buy_Product_InQty.quantity)


                            if order_request_orderItem_quantity <= price_Buy_Product_InQty.quantity:
                                price_Buy_Product_qty -= order_request_orderItem_quantity
                                # price_Buy_Product_InQty.quantity = price_Buy_Product_qty
                                # price_Buy_Product_InQty.save()
                                quantity_to_order_details = order_request_orderItem_quantity
                                order_request_orderItem_quantity = 0
                                print(f"<= {price_Buy_Product_qty}")
                            else:
                                order_request_orderItem_quantity -= price_Buy_Product_qty
                                print(f"> {order_request_orderItem_quantity}")
                                # price_Buy_Product_InQty.quantity = 0
                                # price_Buy_Product_InQty.is_finished = True
                                # price_Buy_Product_InQty.save()
                                quantity_to_order_details = price_Buy_Product_qty

                            # order_details = OrderDetails.objects.create(
                            #     product=product,
                            #     order=new_order,
                            #     name=product.name,
                            #     img=product.product_picture,
                            #     price=order_request_orderItem_price,
                            #     quantity=quantity_to_order_details,
                            #     price_buy=price_Buy_Product_InQty.price_buy,
                            #     dec_product=product.description,
                            #     type_quantity=product.type_quantity,
                            # )
                            # order_details.save()

                    else:
                        return Response(f" {product}ادخل كميه",
                                        status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response(f"الكميه {product} غير كافيه باقى {total_quantity_price_Buy}", status=status.HTTP_400_BAD_REQUEST)


            print("saaaaaaaaaaam")
            return Response(status=status.HTTP_200_OK)


    def post(self, request):
        print(request.data)

        user = request.user
        # print(user+"rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        # print(request.data)
        if user.emp:
            user_man = User.objects.get(id=user.manageid)
            # print("its emp")
        else:
            use = request.user.manageid
            user_man = User.objects.get(id=use)
        # print(user_man)
        manage = UserManage.objects.get(user=user_man)
        print(manage)
        moduler = ModulerUserModel.objects.get(usermanage=manage, id=request.data[0]["moduler"])
        useremp = UserEmployee.objects.get(user=user, usermanager=user_man, time_finshe=False)

        if not MandobClosedDay.objects.filter(usermanage=user_man, is_finished=False, moduler=moduler).exists():
            closeDay = MandobClosedDay()
            closeDay.usermanage = user_man
            closeDay.moduler = moduler
            closeDay.save()

        else:
            closeDay = MandobClosedDay.objects.get(usermanage=user_man, is_finished=False, moduler=moduler)

        #
        # if not ClosedEmp.objects.filter(user=user, is_finished=False, moduler=moduler).exists():
        #     print(closeDay)
        #     closedEmp = ClosedEmp()
        #     closedEmp.usermanage = user_man
        #     closedEmp.user = request.user
        #     closedEmp.emp_name = request.user.get_full_name
        #     closedEmp.close_day = closeDay
        #     closedEmp.moduler = moduler
        #     closedEmp.save()
        #     # print(closedEmp)
        #     print("wwwwwwwwwwwwwwwwwwwwwwwwwww")
        # else:
        #     closedEmp = ClosedEmp.objects.get(user=user, is_finished=False, moduler=moduler)
        #     # print(closeDay)
        #     # print(closedEmp)
        #     print("nnnnnnnnnnnnnnnnnnnnnnnn")
        print(self.checkOrder(request.data, user_man, request.user, closeDay, manage).data)
        if self.checkOrder(request.data, user_man, request.user, closeDay, manage).status_code == 200:
            for order_request in request.data:
                moduler_user = ModulerUserModel.objects.get(usermanage=manage, id=order_request["moduler"])
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

                new_order = MandobOrder()
                new_order.user = request.user
                new_order.usermanage = user_man
                new_order.order_date = datetime.datetime.now()
                new_order.is_finished = True
                new_order.barcode_id = order_request_barcode
                new_order.useremployee = useremp
                new_order.close_day = closeDay
                total = sum(order_total)
                stay = order_request_payment - float(sum(order_total))
                new_order.total = total
                new_order.stay = stay
                new_order.moduler = moduler_user
                new_order.Payment = order_request_payment
                print(f"xxxxxxTOTALxxxxxx: {total}")
                print(f"xxxxxxSTAYxxxxxxx: {stay}")
                pro_det = []




                for order_request_orderItem in order_request_orderItems:
                    order_request_orderItem_barcode = order_request_orderItem["product"]
                    order_request_orderItem_price = float(order_request_orderItem["price"])
                    order_request_orderItem_quantity = float(order_request_orderItem["quantity"])
                    order_total.append(order_request_orderItem_quantity*order_request_orderItem_price)
                    # print(order_request_orderItem_barcode)
                    # print(order_request_orderItem_price)

                    product = MandobProducts.objects.get(barcode_id=order_request_orderItem_barcode)

                    Price_Buy_Products = MandobPriceBuyProduct.objects.all().filter(product=product, is_finished=False)
                    # print("Price_Buy_Products################################")
                    total_quantity_price_Buy = 0
                    pro_det = []
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


                                if order_request_orderItem_quantity < price_Buy_Product_InQty.quantity:
                                    price_Buy_Product_qty -= order_request_orderItem_quantity
                                    price_Buy_Product_InQty.quantity = price_Buy_Product_qty
                                    price_Buy_Product_InQty.save()
                                    quantity_to_order_details = order_request_orderItem_quantity

                                    order_request_orderItem_quantity = 0

                                    print(f"<= {price_Buy_Product_qty}")
                                else:
                                    order_request_orderItem_quantity -= price_Buy_Product_qty
                                    # pro_det.append({
                                    #     "quantity": order_request_orderItem_quantity,
                                    #     "price_buy": price_Buy_Product_InQty.price_buy
                                    # })
                                    print(f"> {order_request_orderItem_quantity}")
                                    price_Buy_Product_InQty.quantity = 0
                                    price_Buy_Product_InQty.is_finished = True
                                    price_Buy_Product_InQty.save()
                                    quantity_to_order_details = price_Buy_Product_qty
                                pro_det.append({
                                    "quantity": quantity_to_order_details,
                                    "price_buy": price_Buy_Product_InQty.price_buy
                                })

                                order_details = MandobOrderDetails.objects.create(
                                    # product=product,
                                    mandoborder=new_order,
                                    name=product.name,
                                    img=product.product_picture,
                                    price=order_request_orderItem_price,
                                    quantity=quantity_to_order_details,
                                    price_buy=price_Buy_Product_InQty.price_buy,
                                    dec_product=product.description,
                                    type_quantity=product.type_quantity,
                                )
                                order_details.save()

                        else:
                            return Response(f" {product}ادخل كميه",
                                            status=status.HTTP_400_BAD_REQUEST)

                    else:
                        return Response(f"الكميه {product} غير كافيه باقى {total_quantity_price_Buy}", status=status.HTTP_400_BAD_REQUEST)


                print("saaaaaaaaaaamaaaaannnnnnddddoooobbbb")
                # if order_request["type_order"] == "mandob":
                #     print("in functhion mntgat_mandob")
                #     print(pro_det)
                #     mntgat_mandob(order_request_orderItem_barcode, user_man, moduler_user, order_request["emp_id"], request.user, pro_det, order_request_orderItem["quantity"])

                # if order_request["type_order"] == "clints":
                print("in functhion client")
                print(pro_det)
                clientOrder(request.data, user_man, request.user, order_request["emp_id"], closeDay, manage)
                # order_client(order_request_orderItem_barcode, user_man, moduler_user, order_request["emp_id"], request.user, pro_det, order_request_orderItem["quantity"])



            return Response("تمت عمليه الدفع", status=status.HTTP_201_CREATED)
        else:
            return Response(self.checkOrder(request.data, user_man, request.user, closeDay, manage).data, status=status.HTTP_400_BAD_REQUEST)

##################################################################################
    # def get(self, request):
    #     user = request.user
    #     print(user)
    #     print(request.GET["order_barcode"])
    #
    #     if user.emp:
    #         user_man = User.objects.get(id=user.manageid)
    #         print("its emp")
    #     else:
    #         user_man = request.user.manageid
    #     print(user_man)
    #
    #
    #     ordr = Order.objects.filter(barcode_id=request.GET["order_barcode"], usermanage=user.manageid, moduler=request.GET["moduler"])
    #     if ordr:
    #         order = Order.objects.get(barcode_id=request.GET["order_barcode"])
    #         user_order = User.objects.get(id=order.user_id)
    #
    #         serializer = OrderSerializer(instance=order)
    #
    #         return Response({"order": serializer.data, "user_order": user_order.get_full_name}, status=status.HTTP_200_OK)
    #     else:
    #         return Response("لا يوجد فاتوره", status=status.HTTP_404_NOT_FOUND)
    #
