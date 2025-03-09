import secrets
import string
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .models import Users, SignatureRequest
from .forms import UserForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password    

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
    return render(request, "IroquoisFalls/userhomepage.html", {'user': request.user})

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

@user_passes_test(lambda u: u.is_superuser)
def ApproveDeny(request):
    form1 = SignatureRequest.objects.filter(name='Inter-Institutional Course Registration Form')
    form2 = SignatureRequest.objects.filter(name='Undergraduate General Petition')
    #signature_requests = SignatureRequest.objects.all()
    signature_requests = form1.union(form2)
    
    if request.method == 'POST':
        for signature_request in signature_requests:
            action = request.POST.get(f'action_{signature_request.id}')
            if action == 'approve':
                signature_request.approved = True
            elif action == 'deny':
                signature_request.approved = False
            signature_request.save()
        
        return redirect('adminforms.html')
    return render(request, 'adminforms.html', {'signature_requests':signature_requests})

from django.contrib.auth import authenticate, login

