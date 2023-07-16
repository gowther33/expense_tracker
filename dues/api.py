from django.contrib.auth.decorators import login_required
import datetime
from django.http import JsonResponse
from datetime import timedelta
from income_app.models import IncomeSource
from .models import Due

import json
from django.db.models import Q


@login_required(login_url='login')
def search_due(request):
    if request.method == 'POST':
        query = json.loads(request.body).get('search_query','')

        if query == '':
            return JsonResponse({
                'error':'Not Found'
            })
        
        due = Due.objects.all()

        dues = due.filter(
            Q(amount__istartswith = query) | 
            Q(date__istartswith = query) | 
            Q(description__icontains = query) | 
            Q(source__source__icontains = query)
        )
        
        filtered_results = dues.values('id','amount','description','source__source','date')
		
        return JsonResponse(
            list(filtered_results)
            ,safe=False
        )