from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, username, password, **extra_fields)

class Users(AbstractBaseUser):  
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=20)
    FirstName = models.CharField(max_length=25, default="First")  # Default Value
    LastName = models.CharField(max_length=25, default="Last")  # Default Value
    phone_number = models.BigIntegerField(default= "0000000000")  # Allow NULL
    address = models.TextField(default="Unknown Address")  # Default Value
    DoB = models.DateField(null=True, blank=True)  # Allow NULL
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class SignatureRequest(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    document_path = models.FileField(upload_to='documents/', null=True, blank=True)
    signed_document = models.FileField(upload_to='signed_documents/', null=True, blank=True)
    signed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Request by {self.user.username} for approval"