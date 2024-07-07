from app import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # TokenRefreshView,
)


urlpatterns = [
    path('', views.getRoutes, name="getRoutes"),
    path('data/', views.DataView.as_view(), name="getData"),
    path('data/<int:pk>', views.DataView.as_view(), name="getData"),
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/profile/', views.UserProfileView.as_view(),name='user_profile'),
    path('users/', views.UsersView.as_view(),name='users'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]