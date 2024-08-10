from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from Crew.models import CallCrew
from Crew.models import TrafficCrew
from Crew.models import TrafficCrewAvailable
from .models import CallDetails

from .forms import CallDetailsForm

from .utils import get_location_coordinates

# from Ambulance.models import AmbulanceDetail
# from Ambulance.models import AmbulanceLocation


# Create your views here.
@login_required
def work_view(request):
    user = request.user

    if CallCrew.objects.filter(user=user).exists():
        if request.method == "POST":
            form = CallDetailsForm(request.POST)

            if form.is_valid():
                call_details = form.save(commit=False)
                call_details.user = user
                call_details.save()

                # Process assigned crew
                selected_crew = form.cleaned_data["assigned_crew"]
                call_details.assigned_crew.set(selected_crew)
                call_details.save()

                # Update crew status to 'active'
                for crew in selected_crew:
                    TrafficCrewAvailable.objects.filter(traffic_crew=crew).update(
                        status="active"
                    )

                return redirect("work_view")
        else:
            form = CallDetailsForm()

        # Prepare data for the template
        vacant_crew = TrafficCrewAvailable.objects.filter(status="vacant")
        vacant_crew_list = []
        for crew in vacant_crew:
            location_coords = get_location_coordinates(crew.location)
            vacant_crew_list.append(
                {"crew": crew.traffic_crew, "location": location_coords}
            )

        # Prepare data for the active crew section
        active_crew = TrafficCrewAvailable.objects.filter(status="active")
        active_crew_list = []
        for crew in active_crew:
            location_coords = get_location_coordinates(crew.location)
            active_crew_list.append(
                {"crew": crew.traffic_crew, "location": location_coords}
            )

        # Fetch call history for the specific user
        call_history = CallDetails.objects.filter(user=user).order_by("-created_at")

        context = {
            "form": form,
            "vacant_crew_list": vacant_crew_list,
            "user": user,
            "call_history": call_history,
            "active_crew_list": active_crew_list,
        }
        return render(request, "Work/home.html", context)

    elif TrafficCrew.objects.filter(user=user).exists():
        traffic_crew = TrafficCrew.objects.get(user=user)
        return redirect("work_traffic_crew_dashboard", crew_id=traffic_crew.crew_id)

    return redirect("login")


@login_required
def call_details_view(request):
    if request.method == "POST":
        caller_name = request.POST.get("caller_name")
        caller_phonenumber = request.POST.get("caller_phonenumber")
        patients_number = request.POST.get("patients_number")
        patients_condition = request.POST.get("patients_condition")
        available_for_ambulance = request.POST.get("available_for_ambulance") == "yes"
        patient_location = request.POST.get("patient_location")

        CallDetails.objects.create(
            caller_name=caller_name,
            caller_phonenumber=caller_phonenumber,
            patients_number=patients_number,
            patients_condition=patients_condition,
            available_for_ambulance=available_for_ambulance,
            patient_location=patient_location,
            user=request.user,
        )

        return redirect("work_view")  # Redirect to the work view after submission

    return redirect("work_view")


@login_required
def assign_crew_to_call(request, call_id):
    call = get_object_or_404(CallDetails, id=call_id)

    if request.method == "POST":
        crew_id = request.POST.get("crew_id")
        crew = get_object_or_404(TrafficCrew, crew_id=crew_id)
        if call.assigned_crew is None:  # Only assign if no crew is assigned
            call.assigned_crew = crew
            call.save()

    return redirect("work_view")  # Redirect back to the work view


@login_required
def work_traffic_crew_dashboard(request, crew_id):
    # This function is to handle TrafficCrew dashboard separately
    traffic_crew = get_object_or_404(TrafficCrew, crew_id=crew_id)
    context = {
        "traffic_crew": traffic_crew,
    }
    return render(request, "Work/traffic_crew_dashboard.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
