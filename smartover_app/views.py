from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib import messages
from django.utils.timezone import localtime
from user_profile.models import UserProfile
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Sum
import xlwt
# from .utils import queryset_filter
import csv
import pandas as pd
import datetime
# from .utils import expense_send_success_mail,expense_send_error_mail
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from datetime import datetime as datetime_custom, timedelta
from django.db.models import Q


# For admin and users
@login_required(login_url='login')
def tasks_page(request):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''

    # Select open tasks
    tasks = Task.objects.all().order_by('-date').filter(status="Open").order_by("-priority")

    try:

        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime_custom.strptime(request.GET['date_from'],'%Y-%m-%d')
            
            filter_context['date_from'] = request.GET['date_from']
            

            date_from_html = request.GET['date_from']

            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')

                filter_context['date_to'] = request.GET['date_to']
                

                date_to_html = request.GET['date_to']
                tasks = tasks.filter(
                    Q(date__gte = date_from )
                    &
                    Q(date__lte = date_to)
                ).order_by('-date')

            tasks = tasks.filter(
                    date__gte = date_from
                ).order_by('-date')

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            date_to_html = request.GET['date_to']
            date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            tasks = tasks.filter(
                date__lte = date_to
            ).order_by('-date')
    
    except:
        messages.error(request,'Something went wrong')
        return redirect('tasks_page')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    paginator = Paginator(tasks,10)
    page_number = request.GET.get('page')
    page_tasks = Paginator.get_page(paginator,page_number)

    if request.user.is_superuser:
        return render(request,'smartover_app/tasks_admin.html',{
            'page_tasks':page_tasks,
            'tasks':tasks,
            'filter_context':filter_context,
            'base_url':base_url,
        })
    else:
        return render(request,'smartover_app/tasks_user.html',{
            'page_tasks':page_tasks,
            'tasks':tasks,
            'filter_context':filter_context,
            'base_url':base_url,
        })

# For admin and users closed task page view
@login_required(login_url='login')
def closed_task_page(request):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''

  
    tasks = Task.objects.all().order_by('-date').filter(status="Closed").order_by("-priority")

    try:

        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime_custom.strptime(request.GET['date_from'],'%Y-%m-%d')
            
            filter_context['date_from'] = request.GET['date_from']
            

            date_from_html = request.GET['date_from']

            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')

                filter_context['date_to'] = request.GET['date_to']
                

                date_to_html = request.GET['date_to']
                tasks = tasks.filter(
                    Q(date__gte = date_from )
                    &
                    Q(date__lte = date_to)
                ).order_by('-date')

            tasks = tasks.filter(
                    date__gte = date_from
                ).order_by('-date')

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            date_to_html = request.GET['date_to']
            date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            tasks = tasks.filter(
                date__lte = date_to
            ).order_by('-date')
    
    except:
        messages.error(request,'Something went wrong')
        return redirect('tasks_page')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    paginator = Paginator(tasks,10)
    page_number = request.GET.get('page')
    page_tasks = Paginator.get_page(paginator,page_number)
    currency = 'PKR - Pakitani Rupee'

    if request.user.is_superuser:
        return render(request,'smartover_app/closed_task_admin.html',{
            'currency':currency,
            'page_tasks':page_tasks,
            'tasks':tasks,
            'filter_context':filter_context,
            'base_url':base_url,
        })
    else:
        return render(request,'smartover_app/closed_task_user.html',{
            'currency':currency,
            'page_tasks':page_tasks,
            'tasks':tasks,
            'filter_context':filter_context,
            'base_url':base_url,
        })



# For Admin and User
@login_required(login_url='login')
def create_task(request):

    context = {
        'values':request.POST
    }

    if request.method == 'GET':
        if request.user.is_superuser:
            return render(request,'smartover_app/create_task_admin.html',context)
        else:
            return render(request,'smartover_app/create_task_user.html',context)

    if request.method == 'POST':
        description = request.POST.get('description','')
        priority = request.POST.get('priority','')

        if description == '':            
            if request.user.is_superuser:
                messages.error(request,'Description cannot be empty')
                return render(request,'smartover_app/tasks_admin.html',context)
            else:
                messages.error(request,'Description cannot be empty')
                return render(request,'smartover_app/tasks_user.html',context)

        if priority != '':
            if priority == "Low":
                priority = 1
            elif priority == "Medium":
                priority = 2
            elif priority == "High":
                priority = 3
            else:
                priority = 4
        else:
            priority = 1


        # Save task
        task_obj = Task.objects.create(
            description=description,
            priority=priority,
            created_by = request.user
        )
        # Redirect
        if request.user.is_superuser:
            messages.success(request,'Task Saved Successfully')
            return redirect('tasks_page')
        else:
            messages.success(request,'Task Saved Successfully')
            return redirect('tasks_page_user')



@login_required(login_url='login')
def view_task(request,id):

    if Task.objects.filter(id=id).exists():
        task = Task.objects.get(id=id)

        context = {
            'task':task,
            'values': task,
        }
        
        if request.method == 'GET':
            if request.user.is_superuser:
                return render(request,'smartover_app/view_task.html',context)
            else:
                return render(request,'smartover_app/view_task_user.html',context)

    else:
        if request.user.is_superuser:
            messages.error(request,'Task does not exists')
            return redirect('tasks_page')
        else:
            messages.error(request,'Task does not exists')
            return redirect('tasks_page_user')


# View for closing task
@login_required(login_url='login')
def view_close(request,id):

    if Task.objects.filter(id=id).exists():
        task = Task.objects.get(id=id)

        context = {
            'task':task,
            'values': task,
        }
        
        if request.method == 'GET':
            if request.user.is_superuser:
                return render(request,'smartover_app/close_task_admin.html',context)
            else:
                return render(request,'smartover_app/close_task_user.html',context)    
        
        if request.method == 'POST':
            remarks = request.POST.get('remarks')

            if remarks != "":
                task.remarks = remarks
            
            # Add closing values
            task.status = "Closed"
            task.closing_date = localtime()
            task.closed_by = request.user
            # Save object
            task.save()
            
            # Redirect
            if request.user.is_superuser:
                messages.success(request,'Task Closed Successfully')
                return redirect('tasks_page')
            else:
                messages.success(request,'Task Closed Successfully')
                return redirect('tasks_page_user')

    else:
        if request.user.is_superuser:
            messages.error(request,'Task does not exists')
            return redirect('tasks_page')
        else:
            messages.error(request,'Task does not exists')
            return redirect('tasks_page_user')


@login_required(login_url='login')
def delete_task(request,id):
    if request.user.is_superuser:
        if Task.objects.filter(id=id).exists():
            task = Task.objects.get(id=id)            

            task.delete()
            messages.success(request,'Task Deleted Successfully')
            return redirect('tasks_page')
        else:
            messages.error(request,'Task does not exists')
            return redirect('tasks_page')
    else:
        messages.error(request,'Only Admin can delete task.')
        return redirect('tasks_page_user')



# @login_required(login_url='login')
# def edit_expense(request,id):
#     if request.user.is_superuser:
#         if Expense.objects.filter(id=id).exists():
#             expense = Expense.objects.get(id=id)
        
#         else:
#             messages.error(request,'Expense does not exists')
#             return redirect('expense')
        
#         categories = ExpenseCategory.objects.all().exclude(id=expense.category.id)

#         context = {
#             'expense':expense,
#             'values': expense,
#             'categories':categories
#         }
        
#         if request.method == 'GET':
#             return render(request,'expense_app/edit_expense.html',context)

#         if request.method == 'POST':
#             amount = request.POST.get('amount','')
#             description = request.POST.get('description','')
#             category = request.POST.get('category','')
#             date = request.POST.get('expense_date','')
            
#             if amount== '':
#                 messages.error(request,'Amount cannot be empty')
#                 return render(request,'expense_app/edit_expense.html',context)
            
#             amount = float(amount)
#             if amount <= 0:
#                 messages.error(request,'Amount should be greater than zero')
#                 return render(request,'expense_app/edit_expense.html',context)
            
#             if description == '':
#                 messages.error(request,'Description cannot be empty')
#                 return render(request,'expense_app/edit_expense.html',context)
            
#             if category == '':
#                 messages.error(request,'ExpenseCategory cannot be empty')
#                 return render(request,'expense_app/edit_expense.html',context)
            
#             if date == '':
#                 date = localtime()
            
#             category_obj = ExpenseCategory.objects.get(name =category)
#             expense.amount = amount
#             expense.date = date
#             expense.category = category_obj
#             expense.description = description
#             expense.save() 
            
#             messages.success(request,'Expense Updated Successfully')
#             return redirect('expense')
#     else:
#         messages.error(request,'Only Admin can edit expense.')
#         return redirect('expense_user')
