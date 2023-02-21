"""Hikaro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('forgot/', views.forgot, name= 'forgot'),
    path('game/', views.game, name= 'game'),    
    path('', views.login_view, name= 'login'),
    path('', views.logout_view, name= 'logout'),
    path('register2/', views.register2, name= 'register2'),
    path('register/', views.register, name= 'register'),
    path('study/', views.study, name= 'study'),
    path('upload/', views.upload, name= 'upload'),
    path('admin/', admin.site.urls),
]
