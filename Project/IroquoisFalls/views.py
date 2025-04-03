import secrets
import string
import os
import subprocess
import base64
import json
import shutil
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.urls import reverse
from .models import Users, StatusRequest, Signature
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password 
from django.core.files.base import ContentFile
from django.conf import settings
from subprocess import run
from django.views.decorators.csrf import csrf_exempt

# Redirect users after login based on `is_admin`
@login_required(login_url='/accounts/login/')
def route_after_login(request):
    try:
        user = Users.objects.get(username=request.user.username)  
        if user.is_admin:  
            return redirect('admindash')  
        else:  
            return redirect('userhomepage')  
    except Users.DoesNotExist:
        return redirect('account_logout')  


# Homepage (Requires Login)
def homepage(request):
    return render(request, "IroquoisFalls/homepage.html", {'user': request.user})


# User Homepage (for non-admins)
@login_required
def user_homepage(request):
    try:
        user = request.user
        statreqs = StatusRequest.objects.filter(user=user)
    except StatusRequest.DoesNotExist:
        raise Http404("Object not found")
    
    assignForms()
    return render(request, "IroquoisFalls/userhomepage.html", {
        'user': request.user, 
        'statreqs': statreqs})
    

def userprofilepage(request):
    return render(request, "IroquoisFalls/userprofilepage.html", {'user': request.user})

# Logout View
def custom_logout(request):
    logout(request)
    return redirect('account_login')

# User Registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_login')  
    else:
        form = UserCreationForm()
    return render(request, "IroquoisFalls/register.html", {"form": form})

# Admin Dashboard
@login_required
def AdminDash(request):
    return render(request, "IroquoisFalls/AdminDash.html", {
        'Users': Users.objects.all()
    })

@login_required
def AdminForms(request):
    try:
        statreqs = StatusRequest.objects.all()
    except StatusRequest.DoesNotExist:
        raise Http404("Object not found")
    
    return render(request, "IroquoisFalls/AdminForms.html", {
        'Users': Users.objects.all(), 
        'statreqs': statreqs})

# View a Specific User (Admin)
@login_required
def AdminDashViewUser(request, id): 
    user = Users.objects.get(pk=id)
    return render(request, "IroquoisFalls/view_user.html", {"user": user})


# Generate a Random ID
def generate_random_id(length=8):
    return ''.join(secrets.choice(string.digits) for _ in range(length))


# Generate a Secure Random Password
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))


# API to return a random ID
def generate_id(request):
    return JsonResponse({'random_id': generate_random_id()})


# API to return a random password
def generate_password(request):
    return JsonResponse({'random_password': generate_random_password()})


# Add a New User
@login_required
def AddUser(request):   
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = Users(
                id=form.cleaned_data.get('id') or generate_random_id(),
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data.get('password') or generate_random_password()),  # ✅ Hashing the password before saving
                FirstName=form.cleaned_data['FirstName'],
                LastName=form.cleaned_data['LastName'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
                DoB=form.cleaned_data['DoB'],
                is_active=form.cleaned_data['is_active'],
                is_admin=form.cleaned_data['is_admin'],
            )
            new_user.save()
            return render(request, "IroquoisFalls/admin_add_user.html", {
                'form': UserForm(),
                'success': True
            })
    else:
        form = UserForm()
    
    return render(request, "IroquoisFalls/admin_add_user.html", {
        'form': form
    })

# Edit an Existing User
@login_required
def EditUser(request, id):
    User = Users.objects.get(pk=id)  # Retrieve the existing user

    if request.method == 'POST':
        form = UserForm(request.POST, instance=User)  # Use instance to update
        if form.is_valid():
            updated_user = form.save(commit=False)
            updated_user.password = User.password  # Keep the original password
            updated_user.save()
            return render(request, "IroquoisFalls/admin_edit_user.html", {
                'form': form,
                'success': True
            })
        else:
            return render(request, "IroquoisFalls/admin_edit_user.html", {
                'form': form,
                'errors': form.errors  # Pass form errors to the template
            })

    # Handle GET request: Show form with existing user details
    form = UserForm(instance=User)
    return render(request, "IroquoisFalls/admin_edit_user.html", {
        'form': form
    })

# Delete a User
@login_required
def DeleteUser(request, id):
    if request.method == "POST":
        user = Users.objects.get(pk=id)
        user.delete()
    return HttpResponseRedirect(reverse('admindash'))

from django.contrib.auth import authenticate, login
from django.contrib import messages

def my_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, email=email, password=password)  # This hashes the input password and checks

        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            messages.error(request, "Invalid email or password.")  # Show error message

    return render(request, "IroquoisFalls/login.html")

def assignForms():
    users = Users.objects.all()
    
    for user in users:
        if not StatusRequest.objects.filter(user=user, title="inter_institutional_course_registration").exists(): 
            StatusRequest.objects.create(
                user = user,
                title = "inter_institutional_course_registration",
                status = "draft",
            )
        if not StatusRequest.objects.filter(user=user, title="undergraduate_general_petition").exists(): 
            StatusRequest.objects.create(
                user = user,
                title = "undergraduate_general_petition",
                status = "draft",
            )

@csrf_exempt
def save_signature(request):
    if request.method == "POST":
        print(f'post request for {request}')
        data = json.loads(request.body)
        signature_data = data.get('signature')
        username = data.get('username')
        document_title = data.get('document_title', 'Unknown Document')
        
        if signature_data:
            format, imgstr = signature_data.split(';base64,')
            ext = format.split('/')[-1]
            signature_image = ContentFile(base64.b64decode(imgstr), name=f"signature_{username}.png")
            
            existing_signature = Signature.objects.filter(user=request.user, document_title=document_title).first()
            
            if existing_signature:
                existing_signature.signature_image.delete()
                existing_signature.signature_image = signature_image
                existing_signature.save()
            else:
                signature = Signature(user=request.user, signature_image=signature_image, document_title=document_title)
                signature.save()
            
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})
     
def latPdf(request, file_name, username):
    BASE_DIR = settings.BASE_DIR
    latex_path = os.path.join(BASE_DIR, 'IroquoisFalls', 'templates', file_name, f'{file_name}.tex')
    pdf_path = os.path.join(BASE_DIR, 'IroquoisFalls', 'templates', file_name, f'{file_name}.pdf')
        
    signed_path = os.path.join(os.path.dirname(latex_path), 'Signed_Forms', f'{file_name}_{username}.tex')
    signed_pdf_path = os.path.join(os.path.dirname(latex_path), 'Signed_Forms', f'{file_name}_{username}.pdf')
    
    shutil.copy(latex_path, signed_path)  
    with open(signed_path, 'r') as f:
        latex_content = f.read()
    latex_content = latex_content.replace("{username}", username)
    with open(signed_path, 'w') as f:
        f.write(latex_content)
    
    if signed_path:
        print(f"signature found for user {username} on document {file_name}.")
        compileLatex = signed_path
    else:
        print(f"No signature found for user {username} on document {file_name}.")
        compileLatex = latex_path
        
    try:
        cwd = os.path.dirname(compileLatex)
        result = subprocess.run(['pdflatex', compileLatex], check=True, cwd=cwd)
        
        if not os.path.exists(pdf_path):
            return HttpResponse('File not found', status=500)
        pdf_file_path = signed_pdf_path if signed_path else pdf_path
    except subprocess.CalledProcessError as e:
        return HttpResponse(f'PDF generation error: {e}', status=500)
    
    with open(pdf_file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename={file_name}_{username}.pdf'
        return response

def update_status(request, statreq_id, action):
    statreq = get_object_or_404(StatusRequest, id=statreq_id)
    
    if request.method == 'POST':
        valid_actions = {
            'submit': 'pending',
            'cancel': 'draft'
        }
        if action in valid_actions:
            new_status = valid_actions[action]
            
            if statreq.status != new_status:
                statreq.status = new_status
                statreq.save()
    return redirect('userhomepage')

def update_status_admin(request, statreq_id, action):
    statreq = get_object_or_404(StatusRequest, id=statreq_id)
    
    if request.method == 'POST':
        valid_actions = {
            'return': 'returned',
            'accept': 'accepted',
            'reject': 'rejected'
        }
        if action in valid_actions:
            new_status = valid_actions[action]
            
            if statreq.status != new_status:
                statreq.status = new_status
                statreq.save()
    return redirect('adminforms')

from django.contrib.auth import authenticate, login
