from django.urls import path
from .views import modulers, addmoduler

urlpatterns = [
    # path("add-cart/", add_to_cart, name="add-cart"),
    # path("cart/", Cart.as_view(), name="cart"),
    path("modulers/", modulers, name="modulers"),
    path("addmoduler<int:modu>", addmoduler, name="addmoduler"),
    # path("backorder/", backorder, name="backorder"),
    # path("backproduct/", backproduct, name="backproduct"),
    # path("closebackorder/", closebackorder, name="closebackorder"),

]