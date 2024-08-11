from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import CallCrew, TrafficCrew, TrafficCrewAvailable

from .forms import (
    CrewLoginForm,
    CallCrewRegisterationForm,
    TrafficCrewRegistrationForm,
    TrafficCrewStatusForm,
)

from Work.views import work_view


def crew_home(request):
    return render(request, "Crew/crew_home.html")


def crew_selection(request):
    return render(request, "Crew/crew_selection.html")


def crew_register(request):
    crew_type = request.GET.get("crew_type")
    form = None

    if request.method == "POST":
        if crew_type == "call":
            form = CallCrewRegisterationForm(request.POST)
            if form.is_valid():
                member = form.save()
                auth_login(request, member.user)
                return redirect("work_view")
        elif crew_type == "traffic":
            form = TrafficCrewRegistrationForm(request.POST)
            if form.is_valid():
                member = form.save()
                auth_login(request, member.user)
                return redirect("traffic_crew_dashboard", crew_id=member.crew_id)
        else:
            return render(request, "Crew/invalid_selection.html")

    if crew_type == "call":
        form = CallCrewRegisterationForm()
        template_name = "Crew/register_call_crew.html"
    elif crew_type == "traffic":
        form = TrafficCrewRegistrationForm()
        template_name = "Crew/register_traffic_crew.html"
    else:
        template_name = "Crew/invalid_selection.html"

    return render(request, template_name, {"form": form})


def crew_login(request):
    if request.method == "POST":
        form = CrewLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Check for CallCrew
                try:
                    CallCrew.objects.get(user=user)
                    return redirect("work_view")
                except CallCrew.DoesNotExist:
                    pass  # Proceed to the next check if CallCrew does not exist
                
                # Check for TrafficCrew
                try:
                    traffic_crew = TrafficCrew.objects.get(user=user)
                    return redirect("crew:traffic_crew_dashboard", crew_id=traffic_crew.crew_id)
                except TrafficCrew.DoesNotExist:
                    # Handle case where neither CallCrew nor TrafficCrew exists
                    return redirect("default_dashboard")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = CrewLoginForm()

    response = render(request, "Crew/crew_login.html", {"form": form})
    response["Cache-Control"] = "no-store"
    return response




@login_required
def call_crew_dashboard(request, crew_id):
    call_crew = get_object_or_404(CallCrew, crew_id=crew_id)
    # Redirect to the Work app's home page for CallCrew members
    return redirect("work_view")  # Adjust if needed based on your URL patterns


@login_required
def traffic_crew_dashboard(request, crew_id):
    traffic_crew = get_object_or_404(TrafficCrew, crew_id=crew_id)

    try:
        crew_available = TrafficCrewAvailable.objects.get(traffic_crew=traffic_crew)
    except TrafficCrewAvailable.DoesNotExist:
        crew_available = None

    if request.method == "POST":
        form = TrafficCrewStatusForm(request.POST, instance=crew_available)
        if form.is_valid():
            form.save()
            return redirect("traffic_crew_dashboard", crew_id=crew_id)
    else:
        form = TrafficCrewStatusForm(instance=crew_available)

    context = {
        "traffic_crew": traffic_crew,
        "crew_available": crew_available,
        "form": form,
    }
    return render(request, "Crew/traffic_crew_dashboard.html", context)


@login_required
def default_dashboard(request):
    return render(request, "Crew/default_dashboard.html")


def crew_logout(request):
    logout(request)
    return redirect("crew:crew_login")


@login_required
def update_status(request):
    if request.method == "POST":
        form = TrafficCrewStatusForm(request.POST)
        if form.is_valid():
            traffic_crew_id = form.cleaned_data.get('traffic_crew_id')
            status = form.cleaned_data.get('status')

            # Ensure that traffic_crew_id is not None and status is valid
            if traffic_crew_id:
                traffic_crew = get_object_or_404(TrafficCrewAvailable, traffic_crew_id=traffic_crew_id)
                traffic_crew.status = status
                traffic_crew.save()
                return redirect('crew:traffic_crew_dashboard', crew_id=traffic_crew.traffic_crew.crew_id)
    else:
        form = TrafficCrewStatusForm()

    return redirect('crew:traffic_crew_dashboard')
