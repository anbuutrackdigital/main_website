from django.urls import path
from . import views

app_name = 'crew'

urlpatterns = [
    path('', views.crew_home, name='crew_home'),
    path('selection/', views.crew_selection, name='crew_selection'),
    path('register/', views.crew_register, name='register_crew'),
    path('login/', views.crew_login, name='crew_login'),
    path('logout/', views.crew_logout, name='crew_logout'),
    path('update-status/', views.update_status, name='update_status'),
    path('dashboard/call/<uuid:crew_id>/', views.call_crew_dashboard, name='call_crew_dashboard'),
    path('dashboard/traffic/<uuid:crew_id>/', views.traffic_crew_dashboard, name='traffic_crew_dashboard'),
    path('default/', views.default_dashboard, name='default_dashboard'),
]