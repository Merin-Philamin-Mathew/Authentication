# from django.db import models
# from django.contrib.auth.models import User

# # Create your models here.

# class Data(models.Model):
#     user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
#     productname = models.CharField(max_length=150)
#     image = models.ImageField(null=True, blank=True)
#     price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     _id = models.AutoField(primary_key=True, editable=False)

#     def __str__(self):
#         return self.productname


# ====================================
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self,email,first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(
            email = email, first_name=first_name,
            last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, first_name, last_name, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to='user/profile_pic',null=True, blank=True)

    def __str__(self):
        return str(self.user.first_name)
    