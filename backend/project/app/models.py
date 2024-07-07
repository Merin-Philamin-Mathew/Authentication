from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Data(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    productname = models.CharField(max_length=150)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.productname

