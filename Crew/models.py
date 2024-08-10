from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geomodels
import uuid


# Create your models here.
class CallCrew(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    crew_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20, null=False, blank=True)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.crew_id} - {self.first_name}"


class TrafficCrew(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    crew_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    bike_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.crew_id} - {self.first_name}"


class TrafficCrewAvailable(models.Model):
    STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('active', 'Active'),
    ]

    traffic_crew = models.OneToOneField(
        TrafficCrew, on_delete=models.CASCADE, primary_key=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='vacant')
    location = geomodels.PointField()

    def __str__(self) -> str:
        return f"{self.traffic_crew.crew_id} - {self.status}"
