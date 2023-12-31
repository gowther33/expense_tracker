from django.shortcuts import render, redirect
from .models import IncomeSource,Income
from django.contrib.auth.models import User
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

from dues.models import Due


# Sum all expenses in the page
def income_sum(incomes):
    page_total = 0
    for expense in incomes:
        page_total += expense.amount
    return page_total

@login_required(login_url='login')
def income_page(request):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''

    incomes = Income.objects.all().order_by('-date')

    try:

        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime_custom.strptime(request.GET['date_from'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_from']
            date_from_html = request.GET['date_from']

            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
                filter_context['date_to'] = request.GET['date_to']
                date_to_html = request.GET['date_to']
                incomes = incomes.filter(
                    Q(date__gte = date_from )
                    &
                    Q(date__lte = date_to)
                ).order_by('-date')

            else:
                incomes = incomes.filter(
                    date__gte = date_from
                ).order_by('-date')

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            date_to_html = request.GET['date_to']
            date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            incomes = incomes.filter(
                date__lte = date_to
            ).order_by('-date')
        
    except:
        messages.error(request,'Something went wrong')
        return redirect('income')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    paginator = Paginator(incomes,10)
    page_number = request.GET.get('page')
    page_incomes = Paginator.get_page(paginator,page_number)
    page_total = income_sum(page_incomes) # Sum total
    currency = 'PKR - Pakitani Rupee'

    
    return render(request,'income_app/income.html',{
        'currency':currency,
        'page_incomes':page_incomes,
        'incomes':incomes,
        'filter_context':filter_context,
        'base_url':base_url,
        'page_total':page_total
    })
@login_required(login_url='login')
def income_page_user(request):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''
    # Added
    today = datetime.datetime.now()
    delta = today - timedelta(days=14)
    today = today.strftime("%Y-%m-%d")
    delta = delta.strftime("%Y-%m-%d") 

    incomes = Income.objects.all().order_by('-date')

    try:

        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime_custom.strptime(request.GET['date_from'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_from']
            date_from_html = request.GET['date_from']

            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
                filter_context['date_to'] = request.GET['date_to']
                date_to_html = request.GET['date_to']
                incomes = incomes.filter(
                    Q(date__gte = date_from )
                    &
                    Q(date__lte = date_to)
                ).order_by('-date')

            else:
                incomes = incomes.filter(
                    date__gte = date_from
                ).order_by('-date')

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            date_to_html = request.GET['date_to']
            date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            incomes = incomes.filter(
                date__lte = date_to
            ).order_by('-date')
        else:
            date_from = delta # from
            date_to = today # today
            incomes = incomes.filter(
                Q(date__gte = date_from )
                &
                Q(date__lte = date_to)
            ).order_by('-date')
        
    except:
        messages.error(request,'Something went wrong')
        return redirect('income_user')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    paginator = Paginator(incomes,10)
    page_number = request.GET.get('page')
    page_incomes = Paginator.get_page(paginator,page_number)
    page_total = income_sum(page_incomes) # Sum total
    currency = 'PKR - Pakitani Rupee'

    
    return render(request,'income_app/income_user.html',{
        'currency':currency,
        'page_incomes':page_incomes,
        'incomes':incomes,
        'filter_context':filter_context,
        'base_url':base_url,
        'page_total':page_total
    })

# For Admin
@login_required(login_url='login')
def add_income(request):

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
                return render(request,'income_app/add_income.html',context)
            else:
                return render(request,'income_app/add_income_user.html',context)
        
        if request.method == 'POST':
            total = request.POST.get('total','')
            received = request.POST.get('received','')
            # amount = request.POST.get('amount','')
            description = request.POST.get('description','')
            source = request.POST.get('source','')
            date = request.POST.get('income_date','')
            
            if total == '':
                if request.user.is_superuser:
                    messages.error(request,'Total cannot be empty')
                    return render(request,'income_app/add_income.html',context)
                else:
                    messages.error(request,'Total cannot be empty')
                    return render(request,'income_app/add_income_user.html',context)

            if received == '':
                if request.user.is_superuser:
                    messages.error(request,'Received cannot be empty')
                    return render(request,'income_app/add_income.html',context)
                else:
                    messages.error(request,'Received cannot be empty')
                    return render(request,'income_app/add_income_user.html',context)
            
            total = float(total)
            received = float(received)
            if total<=0 :
                if request.user.is_superuser:
                    messages.error(request,'Total should be greater than zero')
                    return render(request,'income_app/add_income.html',context)
                else:
                    messages.error(request,'Total should be greater than zero')
                    return render(request,'income_app/add_income_user.html',context)                
            
            if description == '':
                if request.user.is_superuser:
                    messages.error(request,'Description cannot be empty')
                    return render(request,'income_app/add_income.html',context)
                else:
                    messages.error(request,'Description cannot be empty')
                    return render(request,'income_app/add_income_user.html',context)
                
            if source == '':
                if request.user.is_superuser:
                    messages.error(request,'IncomeSource cannot be empty')
                    return render(request,'income_app/add_income.html',context)
                else:
                    messages.error(request,'IncomeSource cannot be empty')
                    return render(request,'income_app/add_income_user.html',context)
                
            if date == '':
                date = localtime()
            
            # If received amount is == to total amount then normal
            # Else make due of total - received
            if received == total:
                # source_obj = IncomeSource.objects.get(user=request.user,source =source)
                amount = received
                source_obj = IncomeSource.objects.get(source =source)
                income_obj = Income.objects.create(
                    amount=amount,
                    date=date,
                    description=description,
                    source=source_obj,
                    created_by = request.user.username
                )
                if request.user.is_superuser:
                    messages.success(request,'Income Saved Successfully')
                    return redirect('income')
                else:
                    messages.success(request,'Income Saved Successfully')
                    return redirect('income_user')
            else:
                amount = received
                amount_due = total - received
                # source_obj = IncomeSource.objects.get(user=request.user,source =source)
                source_obj = IncomeSource.objects.get(source =source)
                income_obj = Income(
                    amount=amount,
                    date=date,
                    description=description,
                    source=source_obj,
                    created_by = request.user.username
                )
                income_obj.save()
                # Create Due
                due_obj = Due(
                    amount = amount_due,
                    date = date,
                    description = description,
                    source = income_obj
                )
                due_obj.save()
                # Due.objects.create(
                #     amount = amount_due,
                #     date = date,
                #     description = description,
                #     source = income_obj
                # )
                if request.user.is_superuser:
                    messages.success(request,'Income Saved Successfully')
                    return redirect('income')
                else:
                    messages.success(request,'Income Saved Successfully')
                    return redirect('income_user')

    else:
        if request.user.is_superuser:
            messages.error(request,'Please add a income source first.')
            return redirect('add_income_source')
        else:
            messages.error(request,'Please ask the Admin to add income sources first.')
            return redirect('income_user')

@login_required(login_url='login')
def add_income_source(request):
    if request.user.is_superuser:
        # sources = IncomeSource.objects.filter(user=request.user)
        sources = IncomeSource.objects.all()
        
        context = {
            'sources' : sources,
            'values':request.POST,
            'create':True
        }

        if request.method == 'GET': 
            return render(request,'income_app/income_source_import.html',context)
        
        if request.method == 'POST':
            source = request.POST.get('source','')
            
            if source == '':
                messages.error(request,'IncomeSource cannot be empty')
                return render(request,'income_app/income_source_import.html',context)
            
            source = source.lower().capitalize()
            if IncomeSource.objects.filter(source = source).exists():
                messages.error(request,f'Income Source ({source}) already exists.')
                return render(request,'income_app/income_source_import.html',context)
            
            IncomeSource.objects.create(source = source).save()
            
            messages.success(request,'IncomeSource added')
            return render(request,'income_app/income_source_import.html',{
                'sources' : sources,
                'create':True
            })
    else:
        messages.error(request,'Only Admin can add income source.')
        return redirect('income_user')

@login_required(login_url='login')
def edit_income_source(request,id):
    if request.user.is_superuser:
        if IncomeSource.objects.filter(pk=id).exists():
            source_obj = IncomeSource.objects.get(pk=id)
        else:
            messages.error(request,'Income source does not exists')
            return redirect('add_income_source')
        
        # if source_obj.user != request.user:
        #     messages.error(request,'Something Went Wrong')
        #     return redirect('add_income_source')

        context = {
            'value' : source_obj.source,
            'update':True,
            'id':source_obj.id
        }

        if request.method == 'GET': 
            return render(request,'income_app/income_source_import.html',context)
        
        if request.method == 'POST':
            source = request.POST.get('source','')
            
            context = {
                'value':source,
                'update':True,
                'id':source_obj.id
            }

            if source == '':
                messages.error(request,'IncomeSource cannot be empty')
                return render(request,'income_app/income_source_import.html',context)
            
            source = source.lower().capitalize()
            if IncomeSource.objects.filter(source = source).exists():
                messages.error(request,f'Income Source ({source}) already exists.')
                return render(request,'income_app/income_source_import.html',context)
            
            source_obj.source = source
            source_obj.save()
            
            messages.success(request,'Income Source Updated')
            return redirect('add_income_source')
    else:
        messages.error(request,'Only Admin can edit income sources.')
        return redirect('income_user')

@login_required(login_url='login')
def delete_income_source(request,id):
    if request.user.is_superuser:
        if IncomeSource.objects.filter(pk=id).exists():
            income_source = IncomeSource.objects.get(pk=id)            
            income_source.delete()
            messages.success(request,'Deleted income source')
            return redirect('add_income_source')
        messages.error(request,'Income source does not exists.')
        return redirect('add_income_source')
    else:
        messages.error(request,'Only Admin can delete income sources.')
        return redirect('income_user')        

@login_required(login_url='login')
def edit_income(request,id):
    if request.user.is_superuser:
        if Income.objects.filter(id=id).exists():
            income = Income.objects.get(id=id)
        
        else:
            messages.error(request,'Something went Wrong. Please Try Again')
            return redirect('income')

        # sources = IncomeSource.objects.filter(user=request.user).exclude(id=income.source.id)
        sources = IncomeSource.objects.all().exclude(id=income.source.id)

        context = {
            'income':income,
            'values': income,
            'sources':sources
        }
        
        if request.method == 'GET':
            return render(request,'income_app/edit_income.html',context)

        if request.method == 'POST':
            amount = request.POST.get('amount','')
            description = request.POST.get('description','')
            source = request.POST.get('source','')
            date = request.POST.get('income_date','')
            
            if amount== '':
                messages.error(request,'Amount cannot be empty')
                return render(request,'income_app/edit_income.html',context)
            
            amount = float(amount)
            if amount <= 0:
                messages.error(request,'Amount should be greater than zero')
                return render(request,'income_app/edit_income.html',context)
            
            if description == '':
                messages.error(request,'Description cannot be empty')
                return render(request,'income_app/edit_income.html',context)
            
            if source == '':
                messages.error(request,'Income Source cannot be empty')
                return render(request,'income_app/edit_income.html',context)
            
            if date == '':
                date = localtime()

            income_obj = IncomeSource.objects.get(source=source)
            income.amount = amount
            income.date = date
            income.source = income_obj
            income.description = description
            income.save()

            messages.success(request,'Income Updated Successfully')
            return redirect('income')
    else:
        messages.error(request,'Only Admin can edit income.')
        return redirect('income_user') 

@login_required(login_url='login')
def delete_income(request,id):
    if request.user.is_superuser:
        if Income.objects.filter(id=id).exists():
            income = Income.objects.get(id=id)

            income.delete()
            messages.success(request,'Income Deleted Successfully')
            return redirect('income')
        else:
            messages.error(request,'Something went Wrong. Please Try Again')
            return redirect('income')
    else:
        messages.error(request,'Only Admin can delete income.')
        return redirect('income_user') 

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
    columns = ['Date','Source','Description','Amount','Added_By']
    
    for col_num in range(len(columns)):
        ws.write(row_number,col_num,columns[col_num],fontStyle)
    fontStyle = xlwt.XFStyle()
    
    incomes = queryset_filter(filter_by).order_by('date')
    rows = incomes.values_list('date','source__source','description','amount','created_by')
    for row in rows:
        row_number += 1
        for col_num in range(len(row)):
            ws.write(row_number,col_num,str(row[col_num]),fontStyle)
    
    row_number +=2
    style = xlwt.easyxf('font: colour red, bold True;')
    ws.write(row_number,0,'TOTAL',style)
    ws.write(row_number,3,str(incomes.aggregate(Sum('amount'))['amount__sum']),style)
    wb.save(response)
    return response

@login_required(login_url='login')
def download_as_csv(request,filter_by):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Incomes-'+ str(request.user.username) + '-' + str(localtime()) + ".csv"
    
    writer = csv.writer(response)
    writer.writerow(['Date','Source','Description','Amount','Added_By'])
    
    incomes = queryset_filter(filter_by).order_by('date')
    for income in incomes:
        writer.writerow([income.date,income.source.source,income.description,income.amount,income.created_by])
    
    writer.writerow(['','','',''])
    writer.writerow(['TOTAL','','',str(incomes.aggregate(Sum('amount'))['amount__sum'])])
    return response

@login_required(login_url='login')
def import_income(request):
    return render(request,'income_app/income_source_import.html',{
        'upload':True
    })

@login_required(login_url='login')
def upload_csv(request):

    if request.method == 'POST':
        try:
            csv_file = request.FILES.get('income_csv_file')

            if csv_file == None:
                messages.error(request,'CSV file required')
                return redirect('import_income')

            if not csv_file.name.endswith('.csv'):
                messages.error(request,'Please Upload a CSV file.')
                return redirect('import_income')
            
            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return redirect('import_income')

            csv = pd.read_csv(csv_file)

            if csv.shape[0] > 10:
                messages.error(request,'Please upload a CSV file with less than 10 rows.')
                return redirect('import_income')

            csv.columns = [c.lower() for c in csv.columns]

            if IncomeSource.objects.filter(source='Loaded From Csv'):
                csv_income_source = IncomeSource.objects.get(source='Loaded From Csv')
            else:
                csv_income_source = IncomeSource.objects.create(source='Loaded From Csv')
                csv_income_source.save()

            income_count = 0
            for i,row in csv.iterrows():
                if not pd.isna(row['date']):
                    date = row['date'].split('-')
                    try:
                        date = datetime.date(2000 + int(date[2]) ,int(date[1]),int(date[0]))
                    except:
                        date = datetime.date.today()
                else:
                    date = datetime.date.today()

                if not pd.isna(row['source']):
                    source = row['source'].strip().lower().capitalize()
                    if IncomeSource.objects.filter(source = source).exists():
                        source = IncomeSource.objects.get(source = source)
                    else:
                        source = IncomeSource.objects.create(source = source)
                        source.save()
                else:
                    source = csv_income_source
                
                if not pd.isna(row['description']):
                    description = row['description'].strip()
                else:
                    description = 'Loaded From Csv'
                
                if not pd.isna(row['amount']):
                    Income.objects.create(
                        amount = float(row['amount']),
                        date = date,
                        description = description,
                        source = source
                    ).save()
                    income_count += 1
            
            income_send_success_mail(request,csv_file.name,income_count,'CSV')
            messages.success(request,'Incomes are saved from csv file.')
            return redirect('income')
        
        except Exception as e:
            income_send_error_mail(request,csv_file.name,'CSV')

            messages.error(request,'Please Check if the format of csv file is correct.')
            return redirect('import_income')

@login_required(login_url='login')
def upload_excel(request):

    if request.method == 'POST':
        try:
            excel_file = request.FILES.get('income_excel_file')
            
            if excel_file == None:
                messages.error(request,'Excel file required')
                return redirect('import_income')
                
            if not (excel_file.name.endswith('.xls') or excel_file.name.endswith('.xlsx')):
                messages.error(request,'Please Upload a Excel file.')
                return redirect('import_income')

            if excel_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (excel_file.size/(1000*1000),))
                return redirect('import_income')
            
            if excel_file.name.endswith('.xls'):
                data = xls_get(excel_file, column_limit=4)
            elif excel_file.name.endswith('.xlsx'):
                data = xlsx_get(excel_file, column_limit=4)
            else:
                messages.error(request,'Please Upload a Excel file.')
                return redirect('import_income')
            
            keys_excel = list(data.keys())

            income_excel_data = data[keys_excel[0]]

            try:
                income_excel_data.remove([])
            except:
                pass

            if len(income_excel_data) > 11:
                messages.error(request,'Please upload a excel file with less than 10 rows.')
                return redirect('import_income')

            if IncomeSource.objects.filter(source='Loaded From Excel'):
                excel_income_source = IncomeSource.objects.get(source='Loaded From Excel')
            else:
                excel_income_source = IncomeSource.objects.create(source='Loaded From Excel')
                excel_income_source.save()

            headers = income_excel_data.pop(0)
            headers = [c.lower() for c in headers] 

            if headers != ['date', 'source', 'description', 'amount']:
                income_send_error_mail(request,excel_file.name,'Excel')
                messages.error(request,'Please Check if the format of excel file is correct.')
                return redirect('import_income')

            income_count = 0
            for row in income_excel_data:

                if(len(row) != 4):
                    break

                if not row[0] == '':
                    if isinstance(row[0],datetime.date):
                        date = row[0]
                    else:
                        date = row['date'].split('-')
                        try:
                            date = datetime.date(2000 + int(date[2]) ,int(date[1]),int(date[0]))
                        except:
                            date = datetime.date.today()
                else:
                    date = datetime.date.today()

                if not row[1] == '':
                    source = row[1].strip().lower().capitalize()
                    if IncomeSource.objects.filter(source = source).exists():
                        income_source = IncomeSource.objects.get(source = source)
                    else:
                        income_source = IncomeSource.objects.create(source = source)
                        income_source.save()
                else:
                    income_source = excel_income_source
                
                if not row[2] == '':
                    description = row[2].strip()
                else:
                    description = 'Loaded From Excel'
                
                if not row[3] == '':
                    Income.objects.create(
                        amount = float(row[3]),
                        date = date,
                        description = description,
                        source = income_source
                    ).save()
                    income_count += 1
            
            income_send_success_mail(request,excel_file.name,income_count,'Excel')
            messages.success(request,'Incomes are saved from excel file.')
            return redirect('income')
        
        except Exception as e:
            income_send_error_mail(request,excel_file.name,'Excel')

            messages.error(request,'Please Check if the format of excel file is correct.')
            return redirect('import_income')
