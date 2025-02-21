from django.db import models

class Users(models.Model):
    userName = models.CharField(max_length=30)
    userEmail = models.EmailField()
    role = models.CharField(max_length=30, default="basicuser")
    status = models.BooleanField()
    
    class Meta:
        db_table = "users"
    
    def __str__(self):
        return self.userName

