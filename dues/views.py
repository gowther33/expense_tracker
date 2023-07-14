from django.shortcuts import render, redirect

from .models import Due
from income_app.models import IncomeSource, Income

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from user_profile.models import UserProfile
from django.utils.timezone import localtime
from django.http import HttpResponse
from django.db.models import Sum
import xlwt
from .utils import queryset_filter
import csv
import pandas as pd
import datetime
from .utils import income_send_success_mail,income_send_error_mail
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from datetime import datetime as datetime_custom, timedelta
from django.db.models import Q



# Sum all expenses in the page
def due_sum(dues):
    page_total = 0
    for expense in dues:
        page_total += expense.amount
    return page_total

@login_required(login_url='login')
def due_page(request):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''

    dues = Due.objects.all().order_by('-date')

    try:

        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime_custom.strptime(request.GET['date_from'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_from']
            date_from_html = request.GET['date_from']

            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
                filter_context['date_to'] = request.GET['date_to']
                date_to_html = request.GET['date_to']
                dues = dues.filter(
                    Q(date__gte = date_from )
                    &
                    Q(date__lte = date_to)
                ).order_by('-date')

            else:
                dues = dues.filter(
                    date__gte = date_from
                ).order_by('-date')

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            date_to_html = request.GET['date_to']
            date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            dues = dues.filter(
                date__lte = date_to
            ).order_by('-date')
        
    except:
        messages.error(request,'Something went wrong')
        return redirect('due')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    paginator = Paginator(dues,10)
    page_number = request.GET.get('page')
    page_dues = Paginator.get_page(paginator,page_number)
    page_total = due_sum(page_dues) # Sum total
    currency = 'PKR - Pakitani Rupee'

    
    return render(request,'dues/due.html',{
        'currency':currency,
        'page_dues':page_dues,
        'dues':dues,
        'filter_context':filter_context,
        'base_url':base_url,
        'page_total':page_total
    })
@login_required(login_url='login')
def due_page_user(request):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''
    # Added
    today = datetime.datetime.now()
    delta = today - timedelta(days=14)
    today = today.strftime("%Y-%m-%d")
    delta = delta.strftime("%Y-%m-%d") 

    dues = Due.objects.all().order_by('-date')

    try:

        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime_custom.strptime(request.GET['date_from'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_from']
            date_from_html = request.GET['date_from']

            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
                filter_context['date_to'] = request.GET['date_to']
                date_to_html = request.GET['date_to']
                dues = dues.filter(
                    Q(date__gte = date_from )
                    &
                    Q(date__lte = date_to)
                ).order_by('-date')

            else:
                dues = dues.filter(
                    date__gte = date_from
                ).order_by('-date')

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            date_to_html = request.GET['date_to']
            date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            dues = dues.filter(
                date__lte = date_to
            ).order_by('-date')
        else:
            date_from = delta # from
            date_to = today # today
            dues = dues.filter(
                Q(date__gte = date_from )
                &
                Q(date__lte = date_to)
            ).order_by('-date')
        
    except:
        messages.error(request,'Something went wrong')
        return redirect('due_user')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    paginator = Paginator(dues,10)
    page_number = request.GET.get('page')
    page_dues = Paginator.get_page(paginator,page_number)
    page_total = due_sum(page_dues) # Sum total
    currency = 'PKR - Pakitani Rupee'

    
    return render(request,'dues/due_user.html',{
        'currency':currency,
        'page_dues':page_dues,
        'dues':dues,
        'filter_context':filter_context,
        'base_url':base_url,
        'page_total':page_total
    })

# For Admin
@login_required(login_url='login')
def add_due(request):

    # if IncomeSource.objects.filter(user=request.user).exists():
    if IncomeSource.objects.all().exists():
        
        # sources = IncomeSource.objects.filter(user=request.user)
        sources = IncomeSource.objects.all()

        context = {
            'sources' : sources,
            'values':request.POST
    	}

        if request.method == 'GET':
            if request.user.is_superuser:
                return render(request,'dues/add_due.html',context)
            else:
                return render(request,'dues/add_due_user.html',context)
        
        if request.method == 'POST':
            amount = request.POST.get('amount','')
            description = request.POST.get('description','')
            source = request.POST.get('source','')
            date = request.POST.get('income_date','')
            
            if amount == '':
                if request.user.is_superuser:
                    messages.error(request,'Amount cannot be empty')
                    return render(request,'dues/add_due.html',context)
                else:
                    messages.error(request,'Amount cannot be empty')
                    return render(request,'dues/add_due_user.html',context)
            
            amount = float(amount)
            if amount<=0 :
                if request.user.is_superuser:
                    messages.error(request,'Amount should be greater than zero')
                    return render(request,'dues/add_due.html',context)
                else:
                    messages.error(request,'Amount should be greater than zero')
                    return render(request,'dues/add_due_user.html',context)
                
            
            if description == '':
                if request.user.is_superuser:
                    messages.error(request,'Description cannot be empty')
                    return render(request,'dues/add_due.html',context)
                else:
                    messages.error(request,'Description cannot be empty')
                    return render(request,'dues/add_due_user.html',context)
                
            if source == '':
                if request.user.is_superuser:
                    messages.error(request,'IncomeSource cannot be empty')
                    return render(request,'dues/add_due.html',context)
                else:
                    messages.error(request,'IncomeSource cannot be empty')
                    return render(request,'dues/add_due_user.html',context)
                
            if date == '':
                date = localtime()
            
            # source_obj = IncomeSource.objects.get(user=request.user,source =source)
            source_obj = IncomeSource.objects.get(source =source)
            due_obj = Due.objects.create(
                amount=amount,
                date=date,
                description=description,
                source=source_obj
            )
            if request.user.is_superuser:
                messages.success(request,'Income Saved Successfully')
                return redirect('due')
            else:
                messages.success(request,'Income Saved Successfully')
                return redirect('due_user')

    else:
        if request.user.is_superuser:
            messages.error(request,'Please add a income source first.')
            return redirect('add_due_source')
        else:
            messages.error(request,'Please ask the Admin to add income sources first.')
            return redirect('due_user')


@login_required(login_url='login')
def edit_due(request,id):
    if request.user.is_superuser:
        if Due.objects.filter(id=id).exists():
            due = Due.objects.get(id=id)
        
        else:
            messages.error(request,'Something went Wrong. Please Try Again')
            return redirect('due')

        # sources = IncomeSource.objects.filter(user=request.user).exclude(id=income.source.id)
        # sources = IncomeSource.objects.all().exclude(id=due.source.id)
        source = Income.objects.get(id = due.source.id)

        context = {
            'due':due,
            'values': due,
            'source':source
        }
        
        if request.method == 'GET':
            return render(request,'dues/edit_due.html',context)

        if request.method == 'POST':
            amount = request.POST.get('amount','')
            description = request.POST.get('description','')
            date = request.POST.get('income_date','')
            
            if amount== '':
                messages.error(request,'Amount cannot be empty')
                return render(request,'dues/edit_due.html',context)
            
            amount = float(amount)
            if amount <= 0:
                messages.error(request,'Amount should be greater than zero')
                return render(request,'dues/edit_due.html',context)
            
            if description == '':
                messages.error(request,'Description cannot be empty')
                return render(request,'dues/edit_due.html',context)
            
            
            if date == '':
                date = localtime()

            due.amount = amount
            due.date = date
            due.description = description
            due.save()

            messages.success(request,'Due Updated Successfully')
            return redirect('due')
    else:
        messages.error(request,'Only Admin can edit due.')
        return redirect('due_user') 

@login_required(login_url='login')
def delete_due(request,id):
    if request.user.is_superuser:
        if Due.objects.filter(id=id).exists():
            due = Due.objects.get(id=id)
            due_source = Income.objects.get(id = due.source.id)
            # Add income in due source
            due_source.amount += due.amount
            due_source.save()
            due.delete()
            messages.success(request,'Due Deleted Successfully')
            return redirect('due')
        else:
            messages.error(request,'Something went Wrong. Please Try Again')
            return redirect('due')
    else:
        messages.error(request,'Only Admin can delete due.')
        return redirect('due_user') 


@login_required(login_url='login')
def due_received(request,id):
    if Due.objects.filter(id=id).exists():
        due = Due.objects.get(id=id)
        # Add amount in the income
        due_source = Income.objects.get(id=due.source.id)

        amt = due_source.amount + due.amount
        due_source.amount = amt
        due_source.save()

        # Add received at
        due.received_at = datetime.datetime.now()
        due.save()

        if request.user.is_superuser:
            messages.success(request,'Due Updated Successfully')
            return redirect('due')
        else:
            messages.success(request,'Due Updated Successfully')
            return redirect('due_user')
    else:
        if request.user.is_superuser:
            messages.error(request,'Something went Wrong. Please Try Again')
            return redirect('due')
        else:
            messages.error(request,'Something went Wrong. Please Try Again')
            return redirect('due_user')


@login_required(login_url='login')
def download_as_excel(request,filter_by):
    filter_by = str(filter_by)
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Incomes-'+ str(request.user.username) + '-' + str(localtime())+".xls"
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Incomes')
    
    if filter_by != '':
        ws.write(0,0,f"Incomes in {filter_by.lower().capitalize()}")
    else:
        ws.write(0,0,f"Incomes in Year")
    
    row_number = 1
    fontStyle = xlwt.XFStyle()
    fontStyle.font.bold = True
    columns = ['Date','Source','Description','Amount']
    
    for col_num in range(len(columns)):
        ws.write(row_number,col_num,columns[col_num],fontStyle)
    fontStyle = xlwt.XFStyle()
    
    dues = queryset_filter(filter_by).order_by('date')
    rows = dues.values_list('date','source__source','description','amount')
    for row in rows:
        row_number += 1
        for col_num in range(len(row)):
            ws.write(row_number,col_num,str(row[col_num]),fontStyle)
    
    row_number +=2
    style = xlwt.easyxf('font: colour red, bold True;')
    ws.write(row_number,0,'TOTAL',style)
    ws.write(row_number,3,str(dues.aggregate(Sum('amount'))['amount__sum']),style)
    wb.save(response)
    return response

@login_required(login_url='login')
def download_as_csv(request,filter_by):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Incomes-'+ str(request.user.username) + '-' + str(localtime()) + ".csv"
    
    writer = csv.writer(response)
    writer.writerow(['Date','Source','Description','Amount'])
    
    dues = queryset_filter(filter_by).order_by('date')
    for due in dues:
        writer.writerow([due.date,due.source.source,due.description,due.amount])
    
    writer.writerow(['','','',''])
    writer.writerow(['TOTAL','','',str(dues.aggregate(Sum('amount'))['amount__sum'])])
    return response



@login_required(login_url='login')
def due_page_sort(request):

    dues =  Due.objects.all()
    base_url = ''

    try:
    
        if 'amount_sort' in request.GET and request.GET.get('amount_sort'):
            base_url = f'?amount_sort={request.GET.get("amount_sort",2)}&'
            if int(request.GET.get('amount_sort',2)) == 1:
                dues = dues.order_by('-amount')
            elif int(request.GET.get('amount_sort',2)) == 2:
                dues = dues.order_by('amount')
        
        if 'date_sort' in request.GET and request.GET.get('date_sort'):
            base_url = f'?date_sort={request.GET.get("date_sort",2)}&'
            if int(request.GET.get('date_sort',2)) == 1:
                dues = dues.order_by('-date')
            elif int(request.GET.get('date_sort',2)) == 2:
                dues = dues.order_by('date')

    except:
        messages.error(request,'Something went wrong')
        return redirect('due')
    
    paginator = Paginator(dues,5)
    page_number = request.GET.get('page')
    page_dues = Paginator.get_page(paginator,page_number)
    currency = 'PKR - Pakistani Rupee'


    return render(request,'income_app/income.html',{
        'currency':currency,
        'page_dues':page_dues,
        'dues':dues,
        'base_url':base_url
    })