from django.urls import path
from .views import productsView, CatgoryProductTypeViw, Cart, orderxx, backorder, backproduct, closebackorder

urlpatterns = [
    # path("add-pro/", productsView.as_view(), name="add-pro"),
    path("pro/", productsView.as_view(), name="pro"),
    path("catgoryproduct/", CatgoryProductTypeViw.as_view(), name="catgoryproduct"),


    path("cart/", Cart.as_view(), name="cart"),
    path("order/", orderxx, name="order"),
    path("backorder/", backorder, name="backorder"),
    path("backproduct/", backproduct, name="backproduct"),
    path("closebackorder/", closebackorder, name="closebackorder"),
]
