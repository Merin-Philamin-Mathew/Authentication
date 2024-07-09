# from rest_framework import serializers 
# from .models import Data
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import RefreshToken


# class DataSerializers(serializers.ModelSerializer):
#     dlsf = 34
#     class Meta:
#         model= Data
#         fields= '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField(read_only=True)
#     _id = serializers.SerializerMethodField(read_only=True)
#     isAdmin = serializers.SerializerMethodField(read_only=True)


#     class Meta:
#         model= User
#         fields= ['_id','id','username','email','name','isAdmin']

#     def get_name(self, obj):
#         firstname = obj.first_name
#         lastname = obj.last_name
#         name = f"{firstname} {lastname}"
#         if name.strip() == "":
#             name = obj.email.split('@')[0]
#         return name
    
#     def get__id(self,obj):
#         return obj.id
    
#     def get_isAdmin(self,obj):
#         return obj.is_staff

# class UserSerializersWithToken(serializers.ModelSerializer):
#     token = serializers.SerializerMethodField(read_only=False)
#     class Meta:
#         model= User
#         # fields= ['_id','id','username','email','name','isAdmin','token']
#         # fields= ['id','username','email','isAdmin','token']
#         fields = '__all__'

#     def get_token(self,obj):
#         token = RefreshToken.for_user(obj)
#         return str(token.access_token)

from rest_framework import serializers
from .models import CustomUser
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'is_staff', 'password']

class UserUpdateSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=True)
    class Meta:
        model = UserProfile
        fields = ['profile_pic']