from .models import *
from django import forms


# class SinUpForms(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ("city", "address", "img", "phone")
#         # fields = "__all__"

class UserForms(forms.ModelForm):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ("first_name", "last_name", "email", "password")

class LoginForms(forms.ModelForm):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ("email", "password")


class EventForms(forms.ModelForm):
    class Meta:
        model = UserManage
        fields = "__all__"
