from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from .models import Task
import json
from django.db.models import Q


@login_required(login_url='login')
def search_task(request):
    if request.method == 'POST':
        query = json.loads(request.body).get('search_query','')

        if query == '':
            return JsonResponse({
                'error':'Not Found'
            })

        task = Task.objects.all()
        
        tasks = task.filter(
            Q(description__icontains = query) |
            Q(priority__icontains = query)
        )



        filtered_results = tasks.values('description', 'created_by__username', 'priority', 'date')
		
        return JsonResponse(
            list(filtered_results)
            ,safe=False
        )