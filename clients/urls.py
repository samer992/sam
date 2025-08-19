from django.urls import path
from .views import AddClient, Dof3at

urlpatterns = [

    path("client/", AddClient.as_view(), name="client"),
    path("dof3at/", Dof3at, name="dof3at"),
    # path("profileemp/", profileemp, name="profileemp"),  # clients
    # path("endemp/", endemp, name="endemp"),
    # path("hdoremp/", hdor_emp, name="hdoremp"),
    # path("tozefemploeey/", tozef_emploeey, name="tozefemploeey"),
    # path("profileemp/", profileemp, name="profileemp"),


]