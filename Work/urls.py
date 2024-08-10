from django.urls import path
from . import views
from Tracker.views import index as TrackerIndex

urlpatterns = [
    path("", views.work_view, name="work_view"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path(
        "dashboard/traffic/<uuid:crew_id>/",
        views.work_traffic_crew_dashboard,
        name="work_traffic_crew_dashboard",
    ),
    path("call-details/", views.call_details_view, name="call_details"),
    path(
        "assign-crew/<int:call_id>/",
        views.assign_crew_to_call,
        name="assign_crew_to_call",
    ),
    path("tracker", TrackerIndex, name='tracker')
]
