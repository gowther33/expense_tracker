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

        task = Task.objects.filter(status='Open')
        
        tasks = task.filter(
            Q(created_by__username = query) |
            Q(description__icontains = query) |
            Q(priority__icontains = query) 
        )



        filtered_results = tasks.values('description', 'created_by__username', 'priority', 'date', 'id')
		
        return JsonResponse(
            list(filtered_results)
            ,safe=False
        )


@login_required(login_url='login')
def search_task_closed(request):
    if request.method == 'POST':
        query = json.loads(request.body).get('search_query','')

        if query == '':
            return JsonResponse({
                'error':'Not Found'
            })

        task = Task.objects.filter(status='Closed')
        
        tasks = task.filter(
            Q(created_by__username = query) |
            Q(description__icontains = query) |
            Q(priority__icontains = query) 
        )



        filtered_results = tasks.values('description', 'created_by__username', 'priority', 'date', 'id', 'status', 'closing_date', 'closed_by__username','remarks')
		
        return JsonResponse(
            list(filtered_results)
            ,safe=False
        )