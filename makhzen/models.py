from time import strftime
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from moduler.models import ModulerUserModel
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
# from creditcards.models import CardNumberField

# Create your models here.
################### ==> Products <== ###################
# from PIL import Image
def upload_to(instance, filename):
    return f"profile_pictures/{strftime('%y/%m/%d')}/{filename}"

class Productsmakhzen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.CharField(max_length=150, verbose_name=_("description"))
    price_sale = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    total_quantity = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    type_quantity = models.CharField(max_length=100, null=True)
    product_picture = models.ImageField(upload_to=upload_to, default="images/bg_1.jpg")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type_id = models.IntegerField(default=1)
    barcode = models.ImageField(upload_to="images/", blank=True)
    barcode_id = models.CharField(max_length=13, null=True)
    total_sale = models.DecimalField(decimal_places=2, max_digits=7, default=0)



    REQUIRED_FIELDS: ["name", "price"]

    def __str__(self):
        return self.name



class PriceBuyProductmakhzen(models.Model):
    product = models.ForeignKey(Productsmakhzen, on_delete=models.CASCADE, related_name="productitemsmakhzen")
    quantity = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    quantity_total = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    price_buy = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    total_buy = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class CatgoryProductTypemakhzen(models.Model):
    # usermanage = models.ForeignKey(User, on_delete=models.CASCADE, related_name="catpromanager")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE, related_name="modulercatgoryitemsmakhzen")

    REQUIRED_FIELDS: ["name", "price"]

    def __str__(self):
        return self.name

################### ==> Order <== ###################

class ClosedDaymakhzen(models.Model):
    usermanage = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)
    # buyManager_total = models.DecimalField(decimal_places=2, max_digits=7, blank=False, default=0)
    # closeDay_total = models.DecimalField(decimal_places=2, max_digits=7, blank=False, default=0)

class ClosedEmpmakhzen(models.Model):
    usermanage = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="usermakhzen")
    # order = models.ManyToManyField(ClosedDay, through="Order")
    close_day = models.ForeignKey(ClosedDaymakhzen, on_delete=models.CASCADE, related_name="closeempitemsmakhzen")
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(auto_now_add=True)
    emp_name = models.CharField(max_length=150, blank=False)


class Ordermakhzen(models.Model):
    usermanage = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ordermanagermakhzen")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orderusermakhzen")
    close_day = models.ForeignKey(ClosedDaymakhzen, on_delete=models.CASCADE)
    close_emp = models.ForeignKey(ClosedEmpmakhzen, on_delete=models.CASCADE, related_name="closeordersitemsmakhzen")
    order_date = models.DateTimeField()
    details = models.ManyToManyField(Productsmakhzen, through="OrderDetailsmakhzen")
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

class OrderDetailsmakhzen(models.Model):
    product = models.ForeignKey(Productsmakhzen, on_delete=models.PROTECT, related_name="orderitemsmakhzen")
    # priceBuyProduct = models.ForeignKey(PriceBuyProduct, on_delete=models.CASCADE)
    order = models.ForeignKey(Ordermakhzen, null=True, on_delete=models.CASCADE, related_name="orderitemsmakhzen")
    name = models.CharField(max_length=150, default="", blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=7, blank=False)
    price_buy = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    quantity = models.DecimalField(decimal_places=2, max_digits=7, default=0.0)
    img = models.CharField(max_length=200, default="", blank=False)
    time = models.DateTimeField(auto_now_add=True)
    type_quantity = models.CharField(max_length=100, null=True)
    dec_product = models.TextField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return "User: " + self.order.user.first_name + "Product: " + self.product.name + ", Order id: " + str(self.order.id)
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


class OrderBackDetailsmakhzen(models.Model):
    is_finished = models.BooleanField(default=False)
    product = models.ForeignKey(Productsmakhzen, on_delete=models.PROTECT, related_name="orderbackitemsmakhzen")
    # priceBuyProduct = models.ForeignKey(PriceBuyProduct, on_delete=models.CASCADE)
    order = models.ForeignKey(Ordermakhzen, null=True, on_delete=models.SET_NULL, related_name="orderbackitemsmakhzen")
    name = models.CharField(max_length=150, default="", blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=7, blank=False)
    price_buy = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    quantity = models.DecimalField(decimal_places=2, max_digits=7, default=0.0)
    img = models.CharField(max_length=200, default="", blank=False)
    time = models.DateTimeField(auto_now_add=True)
    type_quantity = models.CharField(max_length=100, null=True)
    dec_product = models.TextField()
    usermanage = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orderbackmanagermakhzen")
    def __str__(self):
        return "User: " + self.order.user.first_name + "Product: " + self.product.name + ", Order id: " + str(self.order.id)

# class Payment(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     shipment_address = models.CharField(max_length=150)
#     shipment_phone = models.CharField(max_length=50)
#     card_number = CardNumberField()
#     expire =
#     security_code =



