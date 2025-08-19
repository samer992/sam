from django.db import models
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from employee.models import UserEmployee
from moduler.models import ModulerUserModel


# Create your models here.
################### ==> Products <== ###################

class MandobProducts(models.Model):
    usermanage = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mandobproductmanager")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    useremployee = models.ForeignKey(UserEmployee, on_delete=models.CASCADE, related_name="mandobproductemp")
    moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.CharField(max_length=150, verbose_name=_("description"))
    price_sale = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    total_quantity = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    type_quantity = models.CharField(max_length=100, null=True)
    product_picture = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type_id = models.IntegerField(default=1)
    # barcode = models.ImageField(upload_to="images/", blank=True)
    barcode_id = models.CharField(max_length=13, null=True)
    total_sale = models.DecimalField(decimal_places=2, max_digits=7, default=0)

    REQUIRED_FIELDS: ["name", "price"]

    def __str__(self):
        return self.name



class MandobPriceBuyProduct(models.Model):
    product = models.ForeignKey(MandobProducts, on_delete=models.CASCADE, related_name="mandobproductitems")
    quantity = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    quantity_total = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    price_buy = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    total_buy = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# class MandobCatgoryProductType(models.Model):
#     # usermanage = models.ForeignKey(User, on_delete=models.CASCADE, related_name="catpromanager")
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE, related_name="modulercatgoryitems")
#
#     REQUIRED_FIELDS: ["name", "price"]
#
#     def __str__(self):
#         return self.name

################### ==> Order <== ###################
class MandobClosedDay(models.Model):
    usermanage = models.ForeignKey(User, on_delete=models.CASCADE)
    moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)



class MandobOrder(models.Model):
    usermanage = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mandobmanager")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mandobuser")
    moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE)
    useremployee = models.ForeignKey(UserEmployee, on_delete=models.CASCADE)
    close_day = models.ForeignKey(MandobClosedDay, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
    stay = models.DecimalField(decimal_places=2, max_digits=7, blank=False, default=0)
    Payment = models.DecimalField(decimal_places=2, max_digits=7, blank=False, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=7, blank=False, default=0)
    barcode = models.ImageField(upload_to="images/", blank=True, default="profile_pictures/barcode.png")
    barcode_id = models.CharField(max_length=13, null=True)


    def __str__(self):
        return "User: " + self.user.first_name + ", Order id: " + str(self.id)


# مع الدفع########barcode in defulet############
    def save(self, *args, **kwargs):
        options = {
            'format': 'PNG',
            'font_size': 20,
            'text_distance': 2.0,
        }
        EAN = barcode.get_barcode_class("ean13")
        ean = EAN(f"{self.barcode_id}", writer=ImageWriter().set_options(options=options))
        buffer = BytesIO()
        ean.write(buffer)
        # print(File(buffer))
        # self.barcode_id = str(ean)
        self.barcode.save(f"{ean}.svg", File(buffer), save=False)

        return super().save(*args, **kwargs)
# Create your models here.

class MandobOrderDetails(models.Model):
    # product = models.ForeignKey(Products, on_delete=models.PROTECT, related_name="orderitems")
    # priceBuyProduct = models.ForeignKey(PriceBuyProduct, on_delete=models.CASCADE)
    mandoborder = models.ForeignKey(MandobOrder, null=True, on_delete=models.CASCADE, related_name="mandoborderitems")
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
    barcode = models.ImageField(upload_to="images/", blank=True, default="profile_pictures/barcode.png")
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



