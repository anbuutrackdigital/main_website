from django.urls import path
from . import views


urlpatterns = [
    path("",  views.index, name="home"),
    path("register/", views.register_ambulance, name='register_ambulance'),
    path("ambulances", views.ambulance_list, name='ambulance_list'),
    path('ambulances/<str:amb_id>', views.ambulance_detail, name='ambulance_detail'),
]
