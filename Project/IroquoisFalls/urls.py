from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register', views.register, name='register'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.route_after_login, name='route_after_login'),  
    path('userhomepage/', views.user_homepage, name='userhomepage'),
    path('userprofilepage/', views.userprofilepage, name='userprofilepage'),
    path('logout/', views.custom_logout, name='logout'),
    path('admindash/', views.AdminDash, name='admindash'),
    path('adminforms/', views.AdminForms, name='adminforms'),
    path('user/<int:id>/', views.AdminDashViewUser, name="view_user"),
    path('add/', views.AddUser, name="add"),
    path('edit/<int:id>/', views.EditUser, name="edit"),
    path('delete/<int:id>/', views.DeleteUser, name="delete"),
    path('route-after-login/', views.route_after_login, name='route_after_login'),
    #generating ID and password
    path('generate-id/', views.generate_id, name='generate_id'),
    path('generate-password/', views.generate_password, name='generate_password'),
    path('latPdf/<str:file_name>/<str:username>/', views.latPdf, name='latPdf'),
    path('save-signature/', views.save_signature, name='save_signature'),
    path('update-status/<int:statreq_id>/<str:action>/', views.update_status, name='update_status'),
    path('update-status-admin/<int:statreq_id>/<str:action>/', views.update_status_admin, name='update_status_admin'),
]
