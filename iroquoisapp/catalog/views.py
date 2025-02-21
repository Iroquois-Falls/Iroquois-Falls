from django.shortcuts import render, redirect
from django.http import HttpResponse
from catalog.models import Users
from catalog.forms import UserForms

def home_page(request):
    return render(request, 'catalog/home.html')

def create_user(request):
    if request.method == "POST":
        form = UserForms(request.POST)
        if form.is_valid():
                form.save()
                return redirect("users_list")
    else:
        form = UserForms()
    return render(request, "catalog/create.html", {"form": form}) 

def users_list(request):
    users = Users.objects.all()
    return render(request, "catalog/show.html", {"users": users})

def update_user(request, id):
    users = Users.object.get(id=id)
    form = UserForms(request.POST, instance=users)
    if form.is_valid():
        form.save()
        return redirect("home.html")
    return render(request, "catalog/edit.html", {"form":form})
    
def delete(request, userEmail):
    user = Users.objects.get(userEmail = userEmail)
    user.delete()
    return redirect("users_list")