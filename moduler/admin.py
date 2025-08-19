from django.contrib import admin
from .models import ModulerUserModel, ModulerModel
# Register your models here.

admin.site.register(ModulerModel)
admin.site.register(ModulerUserModel)

