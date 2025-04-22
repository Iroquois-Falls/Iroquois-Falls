from django import forms
from .models import Users

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = '__all__'
        exclude = ['password']
        labels = {
            "id": "id",
            "username": "Username",
            "email": "Email",
            "password": "Password",
            "FirstName":"First Name",
            "LastName":"Last Name",
            "phone_number":"Phone Number",
            "address":"Address",
            "DoB": "Date of Birth",
            "is_active": "Is Active",
            "is_admin": "Is Admin",
            "is_manager": "Is Manager",
        }
        widgets = {
            "id": forms.NumberInput(attrs={'class': 'form-control'}),
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "password": forms.PasswordInput(attrs={'class': 'form-control'}),
            "FirstName": forms.TextInput(attrs={'class': 'form-control'}),
            "LastName": forms.TextInput(attrs={'class': 'form-control'}),
            "phone_number": forms.NumberInput(attrs={'class': 'form-control'}),
            "address": forms.TextInput(attrs={'class': 'form-control'}),
            "DoB": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "is_active": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_admin": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_manager": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
