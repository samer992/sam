from django.urls import path
from .views import *

urlpatterns = [
    # path("add-pro/", productsView.as_view(), name="add-pro"),
    # path("pro/", productsView.as_view(), name="pro"),
    # path("catgoryproduct/", CatgoryProductTypeViw.as_view(), name="catgoryproduct"),
    #
    #
    path("tager/", Tager.as_view(), name="tager"),
    path("tagerinvoic/", TagerInvoic.as_view(), name="tagerinvoic"),
    # path("backorder/", backorder, name="backorder"),
    # path("backproduct/", backproduct, name="backproduct"),
    # path("closebackorder/", closebackorder, name="closebackorder"),
    # path("accounting/", AccountingView.as_view(), name="accounting"),
    # path("closeEmp/", close_emp, name="closeEmp"),
    # path("closeDay/", close_day, name="closeDay"),
    # path("closedayaccounting/", close_day_accounting, name="closedayaccounting"),
]


