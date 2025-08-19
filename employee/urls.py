from django.urls import path
from .views import UserEmp, profileemp, endemp, hdor_emp, tozef_emploeey

urlpatterns = [

    path("employee/", UserEmp.as_view(), name="employee"),
    path("profileemp/", profileemp, name="profileemp"),
    path("endemp/", endemp, name="endemp"),
    path("hdoremp/", hdor_emp, name="hdoremp"),
    path("tozefemploeey/", tozef_emploeey, name="tozefemploeey"),
    # path("profileemp/", profileemp, name="profileemp"),


]