import secrets
import string
import os
import subprocess
import base64
import json
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .models import Users, StatusRequest, Signature
from .forms import UserForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password  
from django.core.files.base import ContentFile
from django.conf import settings
from subprocess import run
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from io import BytesIO  

# Redirect users after login based on `is_admin`
@login_required(login_url='/accounts/login/')
def route_after_login(request):
    try:
        user = Users.objects.get(username=request.user.username)  
        if user.is_admin:  
            return redirect('homepage')  
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
        statreqs = StatusRequest.objects.all()
    except StatusRequest.DoesNotExist:
        raise Http404("Object not found")
    
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

def latPdf(request, file_name):
    title_map = {
        'Inter-Institutional Course Registration Form': 'inter_institutional_course_registration',
        'Undergraduate General Petition': 'undergraduate_general_petition',
    }
    
    if file_name not in title_map:
        return HttpResponse('Title not found', status=400)
    
    latex_path = os.path.expanduser(f'~/Project/IroquoisFalls/templates/{file_name}/{file_name}.tex')
    pdf_path = os.path.expanduser(f'~/Project/IroquoisFalls/templates/{file_name}/{file_name}.pdf')
    sig_path = os.path.expanduser(f'~/Project/IroquoisFalls/templates/Signatures/')
    
    db_title = title_map[file_name]
    status_request = StatusRequest.objects.get(title=db_title)
    signature = status_request.signature
    
    if signature:
        signature_image_path = signature.signature_image.path
        dest_path = os.path.join(os.path.dirname(sig_path), "signature.png")
        
        with open(dest_path, 'wb') as f:
            with open(signature_image_path, 'rb') as signature_file:
                f.write(signature_file.read())
    
    try:
        cwd = os.path.dirname(latex_path)
        result = subprocess.run(['pdflatex', latex_path], check=True, cwd=cwd)
        
        if result.stderr:
            return HttpResponse('Compilation error: {result.stderr}', status=500)
        if not os.path.exists(pdf_path):
            return HttpResponse('File not found', status=500)
    except subprocess.CalledProcessError as e:
        return HttpResponse(f'PDF generation error: {e}', status=500)
    
    with open(pdf_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename={file_name}.pdf'
        return response

@csrf_exempt
def save_signature(request):
    if request.method == "POST":
        print(f'post request for {request}')
        data = json.loads(request.body)
        signature_data = data.get('signature')
        document_title = data.get('document_title', 'Unknown Document')
        
        if signature_data:
            format, imgstr = signature_data.split(';base64,')
            ext = format.split('/')[-1]
            signature_image = ContentFile(base64.b64decode(imgstr), name="signature.png")
            
            signature = Signature(user=request.user, signature_image=signature_image, document_title=document_title)
            signature.save()
            
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

from django.contrib.auth import authenticate, login

