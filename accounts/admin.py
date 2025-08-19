from django.contrib import admin
from .models import User, UserManage, Events, Profile, FilesAdmin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(UserManage)
admin.site.register(Events)
admin.site.register(Profile)
admin.site.register(FilesAdmin)
