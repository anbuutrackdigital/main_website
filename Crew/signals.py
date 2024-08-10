from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TrafficCrew, TrafficCrewAvailable


@receiver(post_save, sender=TrafficCrew)
def create_traffic_crew_available(sender, instance, created, **kwargs):
    if created:
        TrafficCrewAvailable.objects.create(
            traffic_crew = instance,
            status = 'vacant',
            location = 'POINT(0 0)'
        )
