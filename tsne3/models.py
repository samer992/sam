from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from moduler.models import ModulerUserModel
from time import strftime

# Create your models here.
################### ==> DortTsne3 <== ###################
class DortTsne3(models.Model):
    usermanage = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dort_tsne3manager")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.CharField(max_length=150, verbose_name=_("description"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Recourses(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    dort_tsne3 = models.ForeignKey(DortTsne3, on_delete=models.CASCADE, related_name="recourses")
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.CharField(max_length=150, verbose_name=_("description"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Tklfa(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    dort_tsne3 = models.ForeignKey(DortTsne3, on_delete=models.CASCADE, related_name="tklfa")
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.CharField(max_length=150, verbose_name=_("description"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


################### ==> ProductsDortTsne3 <== ###################
# from PIL import Image
def upload_to(instance, filename):
    return f"profile_pictures/{strftime('%y/%m/%d')}/{filename}"

class DortTsne3Products(models.Model):
    usermanage = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Dortproductmanager")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dort_tsne3 = models.ForeignKey(DortTsne3, on_delete=models.CASCADE, related_name="antagdorttsne3")
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



class DortTsne3PriceBuyProduct(models.Model):
    product = models.ForeignKey(DortTsne3Products, on_delete=models.CASCADE, related_name="dorttsne3productitems")
    quantity = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    quantity_total = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    price_buy = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    total_buy = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# class CatgoryProductType(models.Model):
#     # usermanage = models.ForeignKey(User, on_delete=models.CASCADE, related_name="catpromanager")
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE, related_name="modulercatgoryitems")
#
#     REQUIRED_FIELDS: ["name", "price"]
#
#     def __str__(self):
#         return self.name
################### ==> Dof3at <== ###################
class Dof3atDortTsne3(models.Model):
    dort_tsne3 = models.ForeignKey(DortTsne3, on_delete=models.CASCADE, related_name="dof3atdorttsne3")
    # name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.CharField(max_length=150, verbose_name=_("description"))
    dof3a = models.DecimalField(decimal_places=2, max_digits=7, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

