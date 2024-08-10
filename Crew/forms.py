from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import TrafficCrew, CallCrew, TrafficCrewAvailable


class CrewLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)


class BaseRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Usernamne already exists")

        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")

        return password2

    def save(self, commit=True):
        # Create the user
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password2"],
        )
        # Create the crew member instance
        crew_member = super().save(commit=False)
        crew_member.user = user
        if commit:
            crew_member.save()

        return crew_member


class CallCrewRegisterationForm(BaseRegistrationForm):
    class Meta:
        model = CallCrew
        fields = ["first_name", "last_name", "phone_number", "gender"]
        User.objects.update()


class TrafficCrewRegistrationForm(BaseRegistrationForm):
    class Meta:
        model = TrafficCrew
        fields = ["first_name", "last_name", "phone_number", "bike_number", "gender"]
        
        
class TrafficCrewStatusForm(forms.ModelForm):
    class Meta:
        model = TrafficCrewAvailable
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=TrafficCrewAvailable.STATUS_CHOICES),
        }
