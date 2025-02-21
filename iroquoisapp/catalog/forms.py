from django import forms
from catalog.models import Users

class UserForms(forms.ModelForm):
    class Meta:
        model = Users
        fields = "__all__"