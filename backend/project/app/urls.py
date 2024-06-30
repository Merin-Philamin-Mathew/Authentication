from app import views
from django.urls import path

urlpatterns = [
    path('', views.getRoutes, name="getRoutes")
]