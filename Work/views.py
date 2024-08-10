from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from Crew.models import CallCrew
from Crew.models import TrafficCrew
from Crew.models import TrafficCrewAvailable

# from Ambulance.models import AmbulanceDetail
# from Ambulance.models import AmbulanceLocation


# Create your views here.
@login_required
def work_view(request):
    user = request.user

    # Check if the user is a CallCrew member
    if CallCrew.objects.filter(user=user).exists():
        # Render the Work app's home page with data for CallCrew members
        traffic_crews = TrafficCrew.objects.all()
        traffic_crew_statuses = TrafficCrewAvailable.objects.all()

        # Create a dictionary for quick lookup of statuses
        status_dict = {status.traffic_crew.crew_id: status.status for status in traffic_crew_statuses}

        combined_data = []
        for traffic_crew in traffic_crews:
            status = status_dict.get(traffic_crew.crew_id, 'unknown')
            combined_data.append({
                'crew_id': traffic_crew.crew_id,
                'name': traffic_crew.first_name,
                'status': status
            })

        context = {
            'combined_data': combined_data,
            'user': user,
        }
        return render(request, 'Work/home.html', context)

    # Check if the user is a TrafficCrew member
    elif TrafficCrew.objects.filter(user=user).exists():
        # Redirect to the TrafficCrew dashboard
        traffic_crew = TrafficCrew.objects.get(user=user)
        return redirect('work_traffic_crew_dashboard', crew_id=traffic_crew.crew_id)
    
    # If user type is unknown or not found, handle accordingly
    return redirect('login')  # Adjust based on your login URL or redirect as needed
    

@login_required
def work_traffic_crew_dashboard(request, crew_id):
    # This function is to handle TrafficCrew dashboard separately
    traffic_crew = get_object_or_404(TrafficCrew, crew_id=crew_id)
    context = {
        "traffic_crew": traffic_crew,
    }
    return render(request, "Work/work_traffic_crew_dashboard.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
