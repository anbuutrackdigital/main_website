from django.urls import path
from . import views

urlpatterns = [
    path('', views.crew_login, name='crew_login'),
    path('logout/', views.crew_logout, name='crew_logout'),
    path('select_crew/', views.crew_selection, name='crew_selection'),
    path('register/', views.crew_register, name='register_crew'),
    path('dashboard/call/<uuid:crew_id>/', views.call_crew_dashboard, name='call_crew_dashboard'),
    path('dashboard/traffic/<uuid:crew_id>/', views.traffic_crew_dashboard, name='traffic_crew_dashboard'),
    path('default_dashboard/', views.default_dashboard, name='default_dashboard'),
]
