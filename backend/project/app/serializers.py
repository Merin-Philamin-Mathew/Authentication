from rest_framework import serializers 
from .models import Data
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class DataSerializers(serializers.ModelSerializer):
    dlsf = 34
    class Meta:
        model= Data
        fields= '__all__'

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model= User
        fields= ['_id','id','username','email','name','isAdmin']

    def get_name(self, obj):
        firstname = obj.first_name
        lastname = obj.last_name
        name = f"{firstname} {lastname}"
        if name.strip() == "":
            name = obj.email.split('@')[0]
        return name
    
    def get__id(self,obj):
        return obj.id
    
    def get_isAdmin(self,obj):
        return obj.is_staff

class UserSerializersWithToken(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['id','username','email']

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)