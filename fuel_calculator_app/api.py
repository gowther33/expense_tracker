from .models import Fuel
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json



@login_required(login_url='login')
def get_fuel(request):
    
    fuel = Fuel.objects.all()


    rate = list(fuel)[0].fuel_rate

    response = {"rate":rate}
    return JsonResponse(
        response
    )


