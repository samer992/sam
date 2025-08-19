from django.urls import path, include
from .views import index, pricing, feature, blog, contact, Admin, dashbord, informathion, handelCartEvent, addCartEvent, \
    handelCartEventEmp, handelCartEventEvents, handelCartEventApp, events, modal

urlpatterns = [
    path("", index, name="home"),
    path("pricing/", pricing, name="pricing"),
    path("modal/", modal, name="modal"),
    path("feature/", feature, name="feature"),
    path("blog/", blog, name="blog"),
    path("contact/", contact, name="contact"),
    path("admin-s/", Admin, name="admin-s"),
    path("dashbord/", dashbord, name="dashbord"),
    path("informathion/", informathion, name="informathion"),
    path("handelCartEvent/<int:add>", handelCartEvent, name="handelCartEvent"),
    path("handelCartEventEmp/<int:add>", handelCartEventEmp, name="handelCartEventEmp"),
    path("handelCartEventEvents/<int:add>", handelCartEventEvents, name="handelCartEventEvents"),
    path("handelCartEventApp/<str:app>", handelCartEventApp, name="handelCartEventApp"),
    path("addCartEvent/", addCartEvent, name="addCartEvent"),
    path("events/<int:id>", events, name="events"),
    # path("num-products/", NumProducts.as_view(), name="num-products"),
    # path("", ProductsGetCreate.as_view()),

]
