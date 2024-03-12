from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('', views.home, name='home'),
]
