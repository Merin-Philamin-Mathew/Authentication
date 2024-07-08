from django.contrib import admin
# from .models import Data

# admin.site.register(Data)
from .models import CustomUser

admin.site.register(CustomUser)