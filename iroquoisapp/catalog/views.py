from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponse
# Create your views here.

def index(request):
    print('Request received')
    return render(request, 'catalog/home.html')
