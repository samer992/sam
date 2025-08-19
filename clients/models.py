from django.db import models
from django.utils.translation import gettext_lazy as _
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from accounts.models import User
from employee.models import UserEmployee
from moduler.models import ModulerUserModel


# Create your models here.

class GroupClients(models.Model):
    usermanage = models.ForeignKey(User, on_delete=models.CASCADE, related_name="groupclientsmanager")
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cgroupclients")
    useremployee = models.ForeignKey(UserEmployee, on_delete=models.CASCADE, related_name="groupclientsemp")
    moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE)
    description = models.CharField(max_length=150, verbose_name=_("description"))
    created_at = models.DateTimeField(auto_now_add=True)
    type_group_clients = models.CharField(max_length=30)
    from_moduler = models.IntegerField(null=True)
    is_agel = models.BooleanField(default=False)


    def __str__(self):
        return self.description

class Client(models.Model):
    usermanage = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clients")
    groupClient = models.ForeignKey(GroupClients, on_delete=models.CASCADE, related_name="groupClients")
    moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE, related_name="groupclient")
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    shop_name = models.CharField(max_length=50, null=True)
    is_agel = models.BooleanField(default=False)
    description = models.CharField(max_length=150, verbose_name=_("description"))
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ClientsOrder(models.Model):
    usermanage = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clientmanager")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clientuser")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="clientorder")
    moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE)
    useremployee = models.ForeignKey(UserEmployee, on_delete=models.CASCADE)
    # close_emp = models.ForeignKey(ClosedEmp, on_delete=models.CASCADE, related_name="closeordersitems")
    order_date = models.DateTimeField()
    # details = models.ManyToManyField(Products, through="ClientsOrderDetails")
    is_finished = models.BooleanField(default=False)
    stay = models.DecimalField(decimal_places=2, max_digits=7, blank=False, default=0)
    Payment = models.DecimalField(decimal_places=2, max_digits=7, blank=False, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=7, blank=False, default=0)
    # barcode = models.ImageField(upload_to="images/", blank=True, default="profile_pictures/barcode.png")
    barcode_id = models.CharField(max_length=13, null=True)

    def __str__(self):
        return "User: " + str(self.client )+ ", Order id: " + str(self.id)


# مع الدفع########barcode in defulet############
#     def save(self, *args, **kwargs):
#         options = {
#             'format': 'PNG',
#             'font_size': 20,
#             'text_distance': 2.0,
#         }
#         EAN = barcode.get_barcode_class("ean13")
#         ean = EAN(f"{self.barcode_id}", writer=ImageWriter().set_options(options=options))
#         buffer = BytesIO()
#         ean.write(buffer)
#         # print(File(buffer))
#         # self.barcode_id = str(ean)
#         self.barcode.save(f"{ean}.svg", File(buffer), save=False)
#
#         return super().save(*args, **kwargs)


# Create your models here.

class ClientsOrderDetails(models.Model):
    # product = models.ForeignKey(Products, on_delete=models.PROTECT, related_name="orderitems")
    # priceBuyProduct = models.ForeignKey(PriceBuyProduct, on_delete=models.CASCADE)
    order = models.ForeignKey(ClientsOrder, null=True, on_delete=models.CASCADE, related_name="clientorderitems")
    name = models.CharField(max_length=150, default="", blank=False)
    # description = models.CharField(max_length=150, verbose_name=_("description"))
    price = models.DecimalField(decimal_places=2, max_digits=7, blank=False)
    price_buy = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    quantity = models.DecimalField(decimal_places=2, max_digits=7, default=0.0)
    img = models.CharField(max_length=200, default="", blank=False)
    time = models.DateTimeField(auto_now_add=True)
    type_quantity = models.CharField(max_length=100, null=True)
    dec_product = models.TextField()
    is_finished = models.BooleanField(default=False)
    # barcode = models.ImageField(upload_to="images/", blank=True, default="profile_pictures/barcode.png")
    barcode_id = models.CharField(max_length=20, null=True)

    def __str__(self):
        return "User: " + self.order.user.first_name + ", Order id: " + str(self.order.id)
    @property
    def get_full_total_sale(self):
        total = self.quantity * self.price
        return total

    @property
    def get_full_total_buy(self):
        total = self.quantity * self.price_buy
        return total
    class Meta:
        ordering = ['-id']



class Dof3atClients(models.Model):

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="dof3atclientorders")
    # order = models.ForeignKey(ClientsOrder, null=True, on_delete=models.CASCADE, related_name="dof3atclientorder")
    useremployee = models.ForeignKey(UserEmployee, on_delete=models.CASCADE)
    # name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.CharField(max_length=150, verbose_name=_("description"))
    dof3a = models.DecimalField(decimal_places=2, max_digits=7, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.dof3a




