from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register', views.register, name='register'),
    path('accounts/profile/', views.route_after_login, name='route_after_login'),  
    path('userhomepage/', views.user_homepage, name='userhomepage'),
    path('userprofilepage/', views.userprofilepage, name='userprofilepage'),
    path('logout/', views.custom_logout, name='account_logout'),
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
    path('latPdf/<str:file_name>/', views.latPdf, name='latPdf'),
    path('save-signature/', views.save_signature, name='save_signature'),
    path('update-status/<int:statreq_id>/', views.update_status, name='update_status'),
    path('cancel-request/<int:statreq_id>/', views.cancel_request, name='cancel_request'),
    path('reject-request/<int:statreq_id>/', views.reject_request, name='reject_request'),
    path('accept-request/<int:statreq_id>/', views.accept_request, name='accept_request'),
    path('return-request/<int:statreq_id>/', views.return_request, name='return_request'),
]
