from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('city/<int:city_id>/', views.city_detail, name='city_detail'),
]