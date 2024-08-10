from django.urls import path
from . import views

urlpatterns = [
    path('', views.work_view, name='work_view'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('dashboard/traffic/<uuid:crew_id>/', views.work_traffic_crew_dashboard, name='work_traffic_crew_dashboard'),
]