from django import forms
from .models import AmbulanceDetail

class AmbulanceForm(forms.ModelForm):
    class Meta:
        model = AmbulanceDetail
        fields = ['amb_num', 'amb_cap', 'amb_hospital']
