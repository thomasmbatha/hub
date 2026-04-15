from django.urls import path
from . import views
# from django.contrib.auth import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vr/', views.vr, name='vr'),
    path('rtl/', views.rtl, name='rtl'),

    
]