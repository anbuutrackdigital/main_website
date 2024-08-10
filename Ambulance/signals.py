from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.geos import Point

from .models import AmbulanceDetail, AmbulanceLocation

@receiver(post_save,sender=AmbulanceDetail)
def create_or_update_ambulance_location(sender, instance, **kwargs):
    location, created = AmbulanceLocation.objects.get_or_create(
        amb_id = instance,
        defaults={'amb_loc': Point(0, 0)}
    )
    
    # update the loction if it exists
    if not created:
        # Optionally update the locaion of perform other logic here
        pass
