from django.contrib.auth.backends import BaseBackend
from .models import Users

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Users.objects.get(email=email, password=password)  # No password hashing
            return user
        except Users.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
