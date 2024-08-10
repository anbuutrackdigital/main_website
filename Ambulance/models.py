from django.db import models
from django.contrib.gis.db import models as geomodels
import uuid


# Create your models here.
class AmbulanceDetail(models.Model):
    amb_id = models.CharField(
        max_length=50, primary_key=True, editable=False, help_text="Unique ambulance id"
    )
    amb_num = models.CharField(
        max_length=20, unique=True, help_text="Ambulance plate number"
    )
    amb_cap = models.PositiveIntegerField(
        help_text="Number of patients an ambulance can carry"
    )
    amb_hospital = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.amb_id:
            self.amb_id = f"{uuid.uuid4()}_{self.amb_num}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.amb_id} - Capacity: {self.amb_num}"


class AmbulanceLocation(models.Model):
    amb_id = models.OneToOneField(
        AmbulanceDetail, on_delete=models.CASCADE, to_field="amb_id", primary_key=True
    )
    amb_loc = geomodels.PointField(help_text="live gps location of the ambulance")

    def __str__(self):
        return f"{self.amb_id} location : ({self.amb_loc.x}, {self.amb_loc.y})"
