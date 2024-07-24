from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
urlpatterns = [
    path('', views.index),
    path('products/', views.product_detail, name='product-list'),              
    path('products/<int:id>/', views.product_detail, name='product-detail'),
    path('login/', TokenObtainPairView.as_view()),
    path('register', views.register),   
]
