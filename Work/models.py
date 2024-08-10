from django.db import models
from django.contrib.auth.models import User

from Crew.models import CallCrew, TrafficCrew, TrafficCrewAvailable
from Ambulance.models import AmbulanceDetail, AmbulanceLocation


# Create your models here.
# models.py
class CallDetails(models.Model):
    caller_name = models.CharField(max_length=100)
    caller_phonenumber = models.CharField(max_length=15)
    patients_number = models.CharField(max_length=15)
    patients_condition = models.TextField()
    available_for_ambulance = models.BooleanField()
    patient_location = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="call_details"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_crew = models.ManyToManyField(
        TrafficCrew, blank=True, related_name="assigned_calls"
    )

    def __str__(self):
        return f"Call from {self.caller_name} at {self.created_at}"


class crewCombineModel(models.Model):
    callCrewDetail = models.ForeignKey(CallCrew, on_delete=models.CASCADE)
    trafficCrewDetail = models.ForeignKey(TrafficCrew, on_delete=models.CASCADE)
    trafficCrewStatus = models.ForeignKey(
        TrafficCrewAvailable, on_delete=models.CASCADE
    )


class ambulanceCombileModel(models.Model):
    ambulanceDetail = models.ForeignKey(AmbulanceDetail, on_delete=models.CASCADE)
    AmbulanceLocation = models.ForeignKey(AmbulanceLocation, on_delete=models.CASCADE)
