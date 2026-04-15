from django.urls import path
from . import views

urlpatterns = [
    path('uniform/', views.uniform, name='uniform'),

    
]