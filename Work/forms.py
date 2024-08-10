# forms.py
from django import forms
from .models import CallDetails, TrafficCrew


class CallDetailsForm(forms.ModelForm):
    assigned_crew = forms.ModelMultipleChoiceField(
        queryset=TrafficCrew.objects.filter(trafficcrewavailable__status="vacant"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = CallDetails
        fields = [
            "caller_name",
            "caller_phonenumber",
            "patients_number",
            "patients_condition",
            "available_for_ambulance",
            "patient_location",
            "assigned_crew",
        ]
