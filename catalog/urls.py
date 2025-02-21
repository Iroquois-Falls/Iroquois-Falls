from django.urls import path
from . import views
from .views import create_user

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("create", views.create_user, name="create_user"),
    path("update", views.update_user, name="update_user"),
]