from django.urls import path
from .views import productsView, CatgoryProductTypeViw, Cart, orderDay, backorder, backproduct, closebackorder, \
    AccountingView, close_emp, close_day, close_day_accounting

urlpatterns = [
    # path("add-pro/", productsView.as_view(), name="add-pro"),
    path("pro/", productsView.as_view(), name="pro"),
    path("catgoryproduct/", CatgoryProductTypeViw.as_view(), name="catgoryproduct"),


    path("cart/", Cart.as_view(), name="cart"),
    path("order/", orderDay, name="order"),
    path("backorder/", backorder, name="backorder"),
    path("backproduct/", backproduct, name="backproduct"),
    path("closebackorder/", closebackorder, name="closebackorder"),
    path("accounting/", AccountingView.as_view(), name="accounting"),
    path("closeEmp/", close_emp, name="closeEmp"),
    path("closeDay/", close_day, name="closeDay"),
    path("closedayaccounting/", close_day_accounting, name="closedayaccounting"),
]


