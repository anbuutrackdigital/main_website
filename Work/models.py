from django.db import models
from Crew.models import CallCrew, TrafficCrew, TrafficCrewAvailable
from Ambulance.models import AmbulanceDetail, AmbulanceLocation


# Create your models here.
class crewCombineModel(models.Model):
    callCrewDetail = models.ForeignKey(CallCrew, on_delete=models.CASCADE)
    trafficCrewDetail = models.ForeignKey(TrafficCrew, on_delete=models.CASCADE)
    trafficCrewStatus = models.ForeignKey(TrafficCrewAvailable, on_delete=models.CASCADE)
    
class ambulanceCombileModel(models.Model):
    ambulanceDetail = models.ForeignKey(AmbulanceDetail, on_delete=models.CASCADE)
    AmbulanceLocation = models.ForeignKey(AmbulanceLocation, on_delete=models.CASCADE)
