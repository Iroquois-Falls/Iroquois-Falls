from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings

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
    ROLE_CHOICES = [
        ('user', 'User'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=20)
    FirstName = models.CharField(max_length=25, default="First")  # Default Value
    LastName = models.CharField(max_length=25, default="Last")  # Default Value
    phone_number = models.BigIntegerField(default= "0000000000")  # Allow NULL
    address = models.TextField(default="Unknown Address")  # Default Value
    DoB = models.DateField(null=True, blank=True)  # Allow NULL
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Signature(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    signature_image = models.ImageField(upload_to='IroquoisFalls/templates/Signatures/', null=True, blank=True)
    document_title = models.CharField(max_length=255)
    signed_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user}'s signature on {self.document_title}"

class StatusRequest(models.Model):
    TITLE_CHOICES = [
        ('inter_institutional_course_registration', 'Inter-Institutional Course Registration Form'),
        ('undergraduate_general_petition', 'Undergraduate General Petition'),
        ('term_withdrawal', 'Term Withdrawal'),
        ('petition_form', 'Petition Form'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('returned', 'Returned'),
        ('rejected', 'Rejected'),
    ]
    
    title = models.CharField(max_length=255, choices=TITLE_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    signature = models.ForeignKey(Signature, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title}: {self.status}"
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'Unknown')

