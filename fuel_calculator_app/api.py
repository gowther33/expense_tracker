from .models import Fuel
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json



@login_required(login_url='login')
def get_fuel(request):
    
    fuel = Fuel.objects.get()

    rate = fuel.fuel_rate
    maintenance = fuel.maintenance_factor
    idling = fuel.idling_factor

    response = {"rate":rate, 'maintenance':maintenance, 'idling':idling}

    return JsonResponse(
        response
    )


