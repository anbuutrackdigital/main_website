from django.contrib import admin
from .models import CallCrew, TrafficCrew, TrafficCrewAvailable

# Register your models here.
admin.site.register(CallCrew)
admin.site.register(TrafficCrew)
admin.site.register(TrafficCrewAvailable)
