from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import CallCrew, TrafficCrew
from .forms import CrewLoginForm, CallCrewRegisterationForm, TrafficCrewRegistrationForm

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
                return redirect("call_crew_dashboard", crew_id=member.crew_id)
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
                try:
                    call_crew = CallCrew.objects.get(user=user)
                    return redirect("call_crew_dashboard", crew_id=call_crew.crew_id)
                except CallCrew.DoesNotExist:
                    try:
                        traffic_crew = TrafficCrew.objects.get(user=user)
                        return redirect("traffic_crew_dashboard", crew_id=traffic_crew.crew_id)
                    except TrafficCrew.DoesNotExist:
                        return redirect("default_dashboard")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = CrewLoginForm()

    response = render(request, "Crew/crew_login.html", {"form": form})
    response['Cache-Control'] = 'no-store'
    return response

@login_required
def call_crew_dashboard(request, crew_id):
    call_crew = get_object_or_404(CallCrew, crew_id=crew_id)
    context = {
        "call_crew": call_crew,
    }
    return render(request, "Crew/call_crew_dashboard.html", context)

@login_required
def traffic_crew_dashboard(request, crew_id):
    traffic_crew = get_object_or_404(TrafficCrew, crew_id=crew_id)
    context = {
        "traffic_crew": traffic_crew,
    }
    return render(request, "Crew/traffic_crew_dashboard.html", context)

@login_required
def default_dashboard(request):
    return render(request, "Crew/default_dashboard.html")

def crew_logout(request):
    logout(request)
    return redirect("crew_login")
