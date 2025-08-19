import datetime

from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import User, UserManage
from accounts.serializers import UserESerializer
from accounts.views import logout
from employee.models import UserEmployee, HadorEmployee
from employee.serializers import UserEmployeeSerializer
from moduler.models import ModulerUserModel
from rest_framework.decorators import api_view, permission_classes, authentication_classes


# Create your views here.
############################################################

class UserEmp(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.manager:

            user_manage = UserManage.objects.get(user=request.user)
            moduler = ModulerUserModel.objects.get(usermanage=user_manage, id=request.data["moduler"])
            # user_man = User.objects.get(user=request.user.manageid)
            access_num_employee = user_manage.num_employee
            # print()
            emps = UserEmployee.objects.filter(usermanager=request.user)
            num_employee = len(emps)
            print(request.data)
            while num_employee < access_num_employee:
                user = User.objects.create_user(
                    first_name=request.data["first_name"],
                    last_name=request.data['last_name'],
                    email=request.data['email'],
                    manageid=request.user.id,
                    password=request.data['password'],
                    is_verified=True,
                    emp=True
                )

                user.save()

                user_emp = UserEmployee()
                user_emp.usermanager = request.user
                user_emp.user = user
                user_emp.full_name = user.get_full_name
                user_emp.email = user.email
                user_emp.moduler = moduler
                user_emp.phone = request.data["phone"]
                user_emp.rqmqume = request.data["rqmqume"]

                user_emp.save()
                print(f"عدد الموظفين لديك {num_employee+1}")
                return Response("تم اضافه الموظف الجديد", status=status.HTTP_201_CREATED)
                break
            else:
                print("end")
                return Response({"m":"خلاص موظفينك ممكن نطمعه نديلو امكانيه يزود فى دوسه ههههههههههههههه"}, status=status.HTTP_200_OK)

        else:
            return Response({"مش مدير"})

    def get(self, request):
        user = request.user
        if user.manager:
            # print(request.GET["moduler"])
            employee = User.objects.filter(emp=True, manageid=user.manageid)
            print(employee)
            serializer = UserESerializer(instance=employee, many=True)
            # print(serializer.data)
            return Response({"employees": serializer.data}, status=status.HTTP_200_OK)

        else:
            return Response("انته مش مدير", status=status.HTTP_423_LOCKED)

    def delete(self, request):
        print(request.GET["iduser"])
        # print(id)
        product_2 = get_object_or_404(UserEmployee, id=request.GET["iduser"])
        print(product_2.user)
        product = get_object_or_404(User, id=product_2.user_id)
        print(product)

        #
        # if product.user != request.user:
        #     return Response({"error": "Sorry you can not update this product"}
        #                     , status=status.HTTP_403_FORBIDDEN)
        #
        product.delete()
        product_2.delete()
        return Response({"details": "Delete action is done"}, status=status.HTTP_200_OK)
        # return Response({"order": "serializer"}, status=status.HTTP_200_OK)
#############################################################

@api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def profileemp(request):
    if request.user.is_authenticated:
        # print(int(request.data["id"]))

        user_manage = UserManage.objects.get(user=request.user)
        moduler = ModulerUserModel.objects.get(usermanage=user_manage, id=request.data["moduler"])
        user_em = User.objects.get(id=request.data["id"])
        print(user_em)
        # employee = UserEmployee.objects.get(usermanager=request.user, time_finshe=False, user=user_em)
        # print(employee.time_finshe)
        # employee.time_finshe = True
        # employee.end_time = datetime.datetime.now()
        # employee.save()


        firstname = request.data["first_name"]
        lastname = request.data["last_name"]
        email = request.data["email"]
        password = request.data["password"]

        # print(user_em)
        user_em.first_name = firstname
        user_em.last_name = lastname
        print(user_em.email)
        print(request.data["rqmqume"])
        if email != user_em.email:
            user_em.email = email

        if not password.startswith('pbkdf2_sha256$'):
            user_em.set_password(password)
        user_em.save()
        if not UserEmployee.objects.filter(user=user_em, time_finshe=False).exists():
            print("user_emp")
            user_emp = UserEmployee()
            user_emp.usermanager = request.user
            user_emp.user = user_em
            user_emp.full_name = user_em.get_full_name
            user_emp.email = user_em.email
            user_emp.moduler = moduler
            user_emp.phone = request.data["phone"]
            user_emp.rqmqume = request.data["rqmqume"]
            user_emp.save()
        else:
            emp = UserEmployee.objects.get(user=user_em, time_finshe=False)
            emp.user = user_em
            emp.full_name = user_em.get_full_name
            emp.email = user_em.email
            # emp.moduler = moduler
            emp.phone = request.data["phone"]
            emp.rqmqume = request.data["rqmqume"]
            emp.save()


        return Response("تم التعديل", status=status.HTTP_201_CREATED)


@api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def endemp(request):
    if request.user.is_authenticated:

        # user_manage = UserManage.objects.get(user=request.user)
        # moduler = ModulerUserModel.objects.get(usermanage=user_manage, id=request.data["moduler"])
        user_em = User.objects.get(id=request.data["id"])
        print(user_em)
        employee = UserEmployee.objects.get(usermanager=request.user, time_finshe=False, user=user_em)
        print(employee.time_finshe)
        employee.time_finshe = True
        employee.end_time = datetime.datetime.now()
        employee.save()
        password = 12345678
        user_em.email = "new@printk.com"
        if not password.startswith('pbkdf2_sha256$'):
            user_em.set_password(password)
        user_em.save()

        return Response("تم التسريح الباسورد الجديد 12345678", status=status.HTTP_200_OK)



@api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def hdor_emp(request):
    if request.user.is_authenticated:
        user_manager = User.objects.get(id=request.user.manageid)
        user_manage = UserManage.objects.get(user=user_manager)
        moduler = ModulerUserModel.objects.get(usermanage=user_manage, id=request.data["moduler"])
        employee = UserEmployee.objects.get(usermanager=user_manager, time_finshe=False, id=request.data["emp_id"])

        hador_employee = HadorEmployee()
        hador_employee.usermanager = user_manager
        hador_employee.user = request.user
        hador_employee.moduler = moduler
        hador_employee.hador = True
        hador_employee.useremployee = employee
        hador_employee.full_name = employee.full_name
        hador_employee.save()

        return Response(f"تم حضور {employee.full_name}", status=status.HTTP_200_OK)




@api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def tozef_emploeey(request):
    user_manager = User.objects.get(id=request.user.manageid)
    work_emploeey = UserEmployee.objects.get(usermanager=user_manager, time_finshe=False, id=request.data["emp_id"])
    work_emploeey.to_moduler = request.data["to_moduler"]
    work_emploeey.type_work = request.data["type_work"]
    work_emploeey.save()

    return Response(f"تم توظيفوووووووو", status=status.HTTP_200_OK)



# @api_view(['POST'])
# # @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def profileemp(request):
#     if request.user.is_authenticated:
#         firstname = request.data["first_name"]
#         lastname = request.data["last_name"]
#         email = request.data["email"]
#         password = request.data["password"]
#         user_emp = User.objects.get(id=request.data["id"])
#         print(user_emp)
#         user_emp.first_name = firstname
#         user_emp.last_name = lastname
#         user_emp.email = email
#
#         if not password.startswith('pbkdf2_sha256$'):
#             user_emp.set_password(password)
#         user_emp.save()
#
#         return Response("انته مش مدير", status=status.HTTP_201_CREATED)

