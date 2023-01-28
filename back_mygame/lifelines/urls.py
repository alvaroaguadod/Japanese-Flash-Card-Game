from django.urls import path
from . import views


#domain.com/lifelines/se define lo siguiente
urlpatterns = [
    path('', views.simple_view)
]
