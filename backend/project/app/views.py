
from .models import CustomUser, UserProfile
from .serializers import UserSerializer, UserUpdateSerializer

from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.middleware import csrf

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
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
        data = request.data
        print(data)
        serializer = UserSerializer(data = data)
        print("serializer vach")
        if serializer.is_valid():
            CustomUser.objects.create_user(email=serializer.validated_data['email'], first_name=serializer.validated_data['first_name'], password=serializer.validated_data['password'], last_name=serializer.validated_data['last_name'])
            print(serializer.data,'serialized data')
            print(data,'user data')
            return Response({'message': 'Data received'}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors)

class LoginView(APIView):
    print('app/view/login')
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        print('app/view/login/post')
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
        refresh["first_name"] = str(user.first_name)
        content = {
            'isAdmin' : user.is_superuser,
        }
        response = Response(content, status = status.HTTP_200_OK)

        response.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE'],
            value = str(refresh.access_token),
            secure= settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.set_cookie(
            key = 'refresh_token',
            value = str(refresh),
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        return response


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
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You are authenticated'})
    
    def post(self, request):
        data = request.data
        # Process the data here
        print("user",request.user)
        print("Headers:", request.headers)
        print("User:", request.user)
        logout(request)
        print("logged out")
        try:
            print('sdlkfls ')
            refresh_token = request.data["refresh_token"]
            print(refresh_token,'token')
            token = RefreshToken(refresh_token)
            print("token",token)
            token.blacklist()
            print("blacklist")
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class MyProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = CustomUser.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response({'message': 'You are authenticated'},serializer.data)
    
        
class UsersView(APIView):
    permission_classes = [AdminOnly]

    def get(self, request):
        user = CustomUser.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
        
                        