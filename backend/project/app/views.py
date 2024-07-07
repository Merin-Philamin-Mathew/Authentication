from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
# from .data import data
from .models import Data
from django.contrib.auth.models import User
from .serializers import DataSerializers, UserSerializer, UserSerializersWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User

# Create your views here.

@api_view(['POST','GET'])
def getRoutes(request):
    return Response("hai")


class DataView(APIView):
    def get(self, request, pk=None):
        if pk:
            # Get a single product
            data = Data.objects.get(_id=pk)
            serializer = DataSerializers(data,many=False)
            return Response(serializer.data)
        
        else:
            datas = Data.objects.all()
            serializer = DataSerializers(datas,many=True)
            return Response(serializer.data)

@permission_classes([IsAuthenticated])
class UserProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    
@permission_classes([IsAuthenticated])
class UsersView(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
            
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username
    #     token['email'] = user.email
    #     # ...

    #     return token
        
    def validate(self, attrs):
        data = super().validate(attrs)
        serializers = UserSerializersWithToken(self.user).data
        for k,v in serializers.items():
            data[k] = v

        return data
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    