from django.shortcuts import render, get_object_or_404, redirect
from .models import AmbulanceDetail, AmbulanceLocation
from .forms import AmbulanceForm
    
def index(request):
    return render(request, 'Ambulance/home.html')

def register_ambulance(request):
    if request.method == 'POST':
        form = AmbulanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ambulance_list')
    else:
        form = AmbulanceForm()
    return render(request, 'Ambulance/register_ambulance.html', {'form': form})

def ambulance_list(request):
    ambulances = AmbulanceDetail.objects.all()
    return render(request, 'Ambulance/ambulance_list.html', {'ambulances': ambulances})

def ambulance_detail(request, amb_id):
    ambulance = get_object_or_404(AmbulanceDetail, amb_id=amb_id)
    location = AmbulanceLocation.objects.filter(amb_id=ambulance).first()
    
    # Use default coordinates (0, 0) if location is not set
    latitude = location.amb_loc.y if location else 0
    longitude = location.amb_loc.x if location else 0
    
    return render(request, 'Ambulance/ambulance_detail.html', {
        'ambulance': ambulance,
        'latitude': latitude,
        'longitude': longitude
    })
