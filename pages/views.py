from moduler.serializer import MoudulerUserSerializer
from shop.models import Products


import datetime

from django.shortcuts import render, redirect

from accounts.models import Events, UserManage, User, FilesAdmin
from moduler.models import ModulerUserModel, ModulerModel
# from productes.models import Products
from pages.models import HandelCartEvent


def index(request):
    context = {
        "file": FilesAdmin.objects.get(title="store-and"),
        # "product": get_object_or_404(productes, pk=id)
    }
    # context = {
    #     "products": Products.objects.all()
    #
    # }


    return render(request, "pages/home.html", context)
def pricing(request):
    context = {
        "events": Events.objects.all(),
        # "product": get_object_or_404(productes, pk=id)
    }


    return render(request, "pages/pricing.html", context)


def modal(request):
    context = {
        "shopename": "Events.objects.all()",
        # "product": get_object_or_404(productes, pk=id)
    }


    return render(request, "pages/informathion.html", context)



def feature(request):

    return render(request, "pages/feature.html")



def blog(request):

    return render(request, "pages/blog.html")


def contact(request):

    return render(request, "pages/contact.html")

def Admin(request):

    return render(request, "pages/admin.html")

def dashbord(request):
    return render(request, "pages/dashbord.html")

# function first event baka

def events(request, id):
    if request.user.is_authenticated:
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" + str(id))
        event = Events.objects.get(id=id)
        user = request.user
        # android = False
        # wep = False


        # if "app" in request.POST:
        #     app = request.POST["app"]
        #     if app == "android":
        #         android = True
        #     if app == "web":
        #         wep = True


        tday = datetime.datetime.now()
        tdelta = datetime.timedelta(days=event.days)
        events = tday + tdelta
        # print(android)
        # print(wep)
        # print(desktop)
        # print(events)
        # print(user)

        user.manager = True
        user.manageid = user.id
        user.save()

        user_man = UserManage()
        user_man.user = request.user
        # user_man.android = android
        # user_man.wep = wep

        user_man.events = events
        user_man.save()
        if request.method == "POST" and "btntgara" in request.POST:
            print("btntgara")
            moduler = ModulerModel.objects.get(name="محل")
            # moduler_emp = ModulerModel.objects.get(name="موظفين")
            print(moduler)

        # if request.method == "POST" and "btntsne3" in request.POST:
        #     print("btntsne3")
        #     moduler = ModulerModel.objects.get(name="تصنيع")
        #     moduler_ma7em = ModulerModel.objects.get(name="مخزن")
        #     moduler_ma7em = ModulerUserModel()
        #     moduler_ma7em.name = moduler.name
        #     moduler_ma7em.namepath = moduler.namepath
        #     moduler_ma7em.imgmoduler = moduler.imgmoduler
        #     moduler_ma7em.usermanage = user_man
        #     moduler_ma7em.save()
            # print(moduler)

        if request.method == "POST" and "btnkhdmat" in request.POST:
            print("btnkhdmat")
            moduler = ModulerModel.objects.get(name="خدمات")
            # moduler_emp = ModulerModel.objects.get(name="موظفين")
            print(moduler)
        add_moduler = ModulerUserModel()
        add_moduler.name = moduler.name
        add_moduler.namee = moduler.namee
        add_moduler.namepath = moduler.namepath
        add_moduler.imgmoduler = moduler.imgmoduler
        add_moduler.usermanage = user_man
        add_moduler.save()
        moduler_emp = ModulerModel.objects.get(name="موظفين")
        add_moduler_emp = ModulerUserModel()
        add_moduler_emp.name = moduler_emp.name
        add_moduler_emp.namee = moduler_emp.namee
        add_moduler_emp.namepath = moduler_emp.namepath
        add_moduler_emp.imgmoduler = moduler_emp.imgmoduler
        add_moduler_emp.usermanage = user_man
        add_moduler_emp.save()
        return redirect("prof")

    else:
        print("nooooooooooooooooo")
        return redirect("signin")







    # return render(request, "pages/home.html")



# #################################################
def addCartEvent(request):
    # events( 1)
    handelCartEvent_check = HandelCartEvent.objects.filter(user=request.user, is_finished=False)
    if handelCartEvent_check:
        handelCartEvent = HandelCartEvent.objects.get(user=request.user, is_finished=False)
        userManage = UserManage.objects.get(user=request.user)
        if handelCartEvent.num_pro_cart != 0:
            userManage.num_products += handelCartEvent.num_pro_cart
            print(handelCartEvent.num_pro_cart)
        if handelCartEvent.num_emp_cart != 0:
            userManage.num_employee += handelCartEvent.num_emp_cart
            print(handelCartEvent.num_emp_cart)
        if handelCartEvent.event_id != 0:
            event_detalis = Events.objects.get(id=handelCartEvent.event_id)

            days = event_detalis.days
            tday = userManage.events
            tdelta = datetime.timedelta(days=days)
            events = tday + tdelta
            # print(events)
            userManage.events = events
        if not userManage.android:
            userManage.android = handelCartEvent.android


        if not userManage.wep:
            userManage.wep = handelCartEvent.wep

        if not userManage.desktop:
            userManage.desktop = handelCartEvent.desktop



        print("addCartEvent")
        userManage.save()
        handelCartEvent.is_finished = True
        handelCartEvent.save()
    else:
        print("no addCartEvent")
    return redirect("informathion")
    # return render(request, "pages/dashbord.html")
def handelCartEvent(request, add):
    # print(add)
    handelCartEvent_check = HandelCartEvent.objects.filter(user=request.user, is_finished=False)
    if handelCartEvent_check:
        handelCartEvent_old = HandelCartEvent.objects.get(user=request.user, is_finished=False)
        if add == 0:
            handelCartEvent_old.num_pro_cart += 1
        else:
            if handelCartEvent_old.num_pro_cart > 0:
                handelCartEvent_old.num_pro_cart -= 1

        handelCartEvent_old.save()


    else:
        handelCartEvent = HandelCartEvent()
        handelCartEvent.user = request.user
        handelCartEvent.num_pro_cart += 1
        handelCartEvent.save()


    return redirect("informathion")
    # return add_num_products


def handelCartEventEmp(request, add):
    # print(add)
    handelCartEvent_check = HandelCartEvent.objects.filter(user=request.user, is_finished=False)
    if handelCartEvent_check:
        handelCartEvent_old = HandelCartEvent.objects.get(user=request.user, is_finished=False)
        if add == 0:
            handelCartEvent_old.num_emp_cart += 1
        else:
            if handelCartEvent_old.num_emp_cart > 0:
                handelCartEvent_old.num_emp_cart -= 1

        handelCartEvent_old.save()


    else:
        handelCartEvent = HandelCartEvent()
        handelCartEvent.user = request.user
        handelCartEvent.num_emp_cart += 1
        handelCartEvent.save()

    return redirect("informathion")


def handelCartEventEvents(request, add):
    print(add)
    handelCartEvent_check = HandelCartEvent.objects.filter(user=request.user, is_finished=False)
    if handelCartEvent_check:
        handelCartEvent_old = HandelCartEvent.objects.get(user=request.user, is_finished=False)
        if handelCartEvent_old.event_id == 0:
            handelCartEvent_old.event_id = add


            handelCartEvent_old.save()


    else:
        handelCartEvent = HandelCartEvent()
        handelCartEvent.user = request.user
        handelCartEvent.event_id = add
        handelCartEvent.save()

    return redirect("informathion")


def informathion(request):
    num_pro_cart = 0
    num_emp_cart = 0
    num_event_cart = 0
    price_event_cart = 0
    events = Events.objects.all()

    modulers_type = ModulerModel.objects.all()

    userManage = UserManage.objects.get(user=request.user)
    usermoduler = ModulerUserModel.objects.filter(usermanage=userManage)
    serializer = MoudulerUserSerializer(instance=usermoduler, many=True)
    print(serializer.data[0]["moduler_profile"][0]["logo_picture"])
    # print(usermoduler[0].modulerprof[0])
    # print(usermoduler[0].modulerprofile[0].shop_name)
    x = []
    for i in usermoduler:
        productes = Products.objects.filter(user=request.user, moduler=i)
        x.append(len(productes))

    num_days = userManage.events.date() - userManage.start_time.date()
    stay_days = userManage.events.date() - datetime.datetime.now().date()

    employees = User.objects.filter(manageid=request.user.id, emp=True)
    # android = userManage.android
    # wep = userManage.wep
    # desktop = userManage.desktop
    # android_price = 0
    # wep_price = 0
    # desktop_price = 0
    # wep_back = True
    # desktop_back = True
    # android_back = True

    handelCartEvent_check = HandelCartEvent.objects.filter(user=request.user, is_finished=False)
    if handelCartEvent_check:

        handelCartEvent = HandelCartEvent.objects.get(user=request.user, is_finished=False)
        if handelCartEvent.event_id != 0:
            event_detalis = Events.objects.get(id=handelCartEvent.event_id)
            num_event_cart = event_detalis.days
            price_event_cart = event_detalis.price

        # if android != handelCartEvent.android:
        #     handelCartEvent.android = True
        #     handelCartEvent.save()
        #
        #     # android = True
        #     if not android:
        #         android_back = False
        #         android_price = 25
        #     print("مشترك")
        # else:
        #     if not android:
        #         # if handelCartEvent.android:
        #
        #         print("from android")
        #     # android = False
        #     print("مش مشترك")
        #
        # print("android")
        # if wep != handelCartEvent.wep:
        #     handelCartEvent.wep = True
        #     handelCartEvent.save()
        #     if not wep:
        #         wep_back = False
        #         print(f"xxxxx wepppp{wep_back}")
        #         wep_price = 30
        #
        #     # wep = True
        #     print("مشترك")
        # else:
        #     if not wep:
        #         # if handelCartEvent.wep:
        #
        #         print("from wep")
        #     # wep = False
        #     print("مش مشترك")
        # print("wep")
        # if desktop != handelCartEvent.desktop:
        #     handelCartEvent.desktop = True
        #     handelCartEvent.save()
        #     if not desktop:
        #         desktop_back = False
        #         desktop_price = 40
        #
        #     # desktop = True
        #     print("مشترك")
        # else:
        #     # desktop = False
        #     if not desktop:
        #         # if handelCartEvent.desktop:
        #         #     desktop_price = 40
        #         print("from desktop")
        #
        #     print("مش مشترك")
        # print("desktop")
        #
        # android = handelCartEvent.android
        # wep = handelCartEvent.wep
        # desktop = handelCartEvent.desktop





        num_pro_cart = handelCartEvent.num_pro_cart
        num_emp_cart = handelCartEvent.num_emp_cart



    price_num_pro_cart = num_pro_cart * 1
    price_num_emp_cart = num_emp_cart * 10
    price_num_event_cart = price_event_cart
    total = price_num_pro_cart + price_num_emp_cart + price_num_event_cart

    # print(wep_back)
    # print(wep)
    context = {
        # "handelCartEvent":
        #     {
        #         "num_pro_cart": num_pro_cart,
        #         "num_emp_cart": num_emp_cart,
        #         "event_id": num_event_cart
        #     },
        # "events": events,
        "num_days": num_days.days,
        "stay_days": stay_days.days,
        "start_time": userManage.start_time.date,
        "last_time": userManage.events.date,
        # "android": android,
        # "wep": wep,
        # "desktop": desktop,
        "num_employee": userManage.num_employee,
        "usermoduler": serializer.data,
        # "modulers_type": modulers_type,
        # "and": userManage.android,
        "num_products_now": x,
        "num_employee_now": len(employees),
        # "total": total,
        # "wep_back": wep_back,
        # "android_back": android_back,
        # "desktop_back": desktop_back,

    }
    return render(request, "pages/informathion.html", context)

def handelCartEventApp(request, app):
    def x(handelCartEvent_old):
        if app == "android":
            if handelCartEvent_old.android:
                handelCartEvent_old.android = False
            else:
                handelCartEvent_old.android = True
            print(app)
        if app == "wep":
            if handelCartEvent_old.wep:
                handelCartEvent_old.wep = False
            else:
                handelCartEvent_old.wep = True
            print(app)
        if app == "desktop":
            if handelCartEvent_old.desktop:
                handelCartEvent_old.desktop = False
            else:
                handelCartEvent_old.desktop = True
            print(app)
        handelCartEvent_old.user = request.user
        handelCartEvent_old.save()
    print(app)
    handelCartEvent_check = HandelCartEvent.objects.filter(user=request.user, is_finished=False)
    if handelCartEvent_check:
        handelCartEvent_old = HandelCartEvent.objects.get(user=request.user, is_finished=False)
        x(handelCartEvent_old)

    else:
        handelCartEvent_new = HandelCartEvent()
        x(handelCartEvent_new)


    return redirect("informathion")

# class products(viewsets.ModelViewSet):
#     queryset = Products.objects.all()
#     serializer_class = ProductsSerilizer
#
#
# class userprof(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerilizer
# # class ProductsGetCreate(generics.ListCreateAPIView):
# #     queryset = Products.objects.all()
# #     serializer_class = ProductsSerilizer
# #
# #
# #
# # class ProductsUpdateDelet(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = Products.objects.all()
# #     serializer_class = ProductsSerilizer
# #
# #
# @api_view(['GET'])
# def new_reservation(request):
#     products_fav = Products.objects.all().order_by("?").first()
#     data = {}
#     if products_fav:
#         # data = model_to_dict(products_fav, fields=["id", "name", "price", "sale_price"])
#         data = ProductsSerilizer(products_fav).data
#
#     return Response(data)
#
#
#
# @api_view(['POST'])
# def post_new_reservation(request):
#     print(request.data)
#     serializer = ProductsSerilizer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         # data = model_to_dict(products_fav, fields=["id", "name", "price", "sale_price"])
#         data = serializer.data
#
#         return Response(data)
#     return Response({"data": "NOT GOOD DATA"})


