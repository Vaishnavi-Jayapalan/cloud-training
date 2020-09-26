from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.AssetView.createAsset),
    path('<int:id>/get/', views.AssetView.getAsset),
]    
