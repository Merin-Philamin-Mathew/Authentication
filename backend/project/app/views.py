# from django.shortcuts import render
# from django.http import JsonResponse
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.views import APIView
# # from .data import data
# from .models import Data
# from django.contrib.auth.models import User
# from .serializers import DataSerializers, UserSerializer, UserSerializersWithToken
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from django.contrib.auth.models import User

# # Create your views here.

# @api_view(['POST','GET'])
# def getRoutes(request):
#     return Response("hai")


# class DataView(APIView):
#     def get(self, request, pk=None):
#         if pk:
#             # Get a single product
#             data = Data.objects.get(_id=pk)
#             serializer = DataSerializers(data,many=False)
#             return Response(serializer.data)
        
#         else:
#             datas = Data.objects.all()
#             serializer = DataSerializers(datas,many=True)
#             return Response(serializer.data)
        


# @permission_classes([IsAuthenticated])
# class UserProfileView(APIView):
#     def get(self, request):
#         user = request.user
#         serializer = UserSerializer(user, many=False)
#         return Response(serializer.data)
    
# @permission_classes([IsAuthenticated])
# class UsersView(APIView):
#     def get(self, request):
#         user = User.objects.all()
#         serializer = UserSerializer(user, many=True)
#         return Response(serializer.data)
            
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         serializers = UserSerializersWithToken(self.user).data
#         for k,v in serializers.items():
#             data[k] = v

#         return data
    
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


from .models import CustomUser, UserProfile
from .serializers import UserSerializer, UserUpdateSerializer
from django.views import View


from django.contrib.auth import authenticate,login,logout

from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser


class AdminOnly(permissions.BasePermission):
    print("app/view/adminOnly")
    def has_permission(self, request, view):
        print("user?staff?",request.user, request.user.is_staff)
        return request.user and request.user.is_staff

class Register(APIView):
    print("app/views/register")
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print("app/views/register")
        data = request.data
        print(data)
        serializer = UserSerializer(data = data)
        
        if serializer.is_valid():
            CustomUser.objects.create_user(email=serializer.validated_data['email'], first_name=serializer.validated_data['first_name'], password=serializer.validated_data['password'], last_name=serializer.validated_data['last_name'])
            print(serializer.data,'lsllsl')
            print(data,'user data')
            return Response({'message': 'Data received'}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors)

class LoginView(APIView):
    print('app/view/login')
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        print('app/view/login')
        email = request.data['email']
        password = request.data['password']
        print(email, password)

        response = Response()

        user = CustomUser.objects.filter(email = email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        login(request, user)
        refresh = RefreshToken.for_user(user)
        refresh['first_name'] = str(user.first_name)
        user_profile = CustomUser.objects.get(email=request.user)
        serializer = UserSerializer(user_profile)

      

        content = {
            'refresh':str(refresh),
            'access':str(refresh.access_token),
            'isAdmin':user.is_superuser,
            "data":serializer.data
        }
    
        return Response(content, status=status.HTTP_200_OK)


class Profile(APIView):
    print('app/view/profile')
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        print('user',request.user)
        user_profile = CustomUser.objects.get(email=request.user)
        serializer = UserSerializer(user_profile)
        print(user_profile,serializer.data)
        return Response({'message':serializer.data}, status=status.HTTP_200_OK)


class UpdateProfile(APIView):
    print('app/view/updateprofile')
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        print("post/request.data",request.data)

        user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        pic = request.data.get('pic')

        if first_name:
            request.user.first_name = first_name
        if last_name:
            request.user.last_name = last_name
        if email:
            request.user.email = email
        request.user.save()

        if pic:
            user_profile.profile_pic = pic
        user_profile.save()
        user_profile = CustomUser.objects.get(email=request.user)
        serializer = UserSerializer(user_profile)
        return Response(serializer.data)

class AdminHome(APIView):
    print("app/view/adminHome")
    permission_classes = [AdminOnly]
    def get(self, request):
        print("app/view/adminHome")
        all_users = CustomUser.objects.all()
        serializer = UserSerializer(all_users, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        print("app/view/logoutView")
        print("user",request.user)
        print("Headers:", request.headers)
        print("User:", request.user)
        logout(request)
        print("logged out")
        try:
            refresh_token = request.data["refresh_token"]
            print(refresh_token,'token')
            token = RefreshToken(refresh_token)
            print("token",token)
            token.blacklist()
            print("blacklist")
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
                        