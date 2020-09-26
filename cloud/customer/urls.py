from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerView.createCustomer),
    path('list/', views.CustomerView.listCustomer),
]    
