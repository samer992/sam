from django.urls import path
from .views import MandobProductsView, get_mandob_products, Cart

urlpatterns = [
    path("mandob-products/", get_mandob_products, name="mandob-products"),
    path("cart/", Cart.as_view(), name="cart"),

    path("mandobproducts/", MandobProductsView.as_view(), name="mandobproducts"),
    # path("addmoduler<int:modu>", addmoduler, name="addmoduler"),


]