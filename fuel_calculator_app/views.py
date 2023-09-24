from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FuelCalculator
from expense_app.models import Expense, ExpenseCategory
import datetime
import json
# Create your views here.



@login_required(login_url='login')
def calculate_fuel(request):

    if request.method == 'GET':
        return render(request, 'fuel_calculator_app/fuel_calculator.html')

    if request.method == 'POST':

        # data = json.loads(request.body.decode('utf-8'))

        # From top html
        # rider = data['rname'] # Pname
        # date = data['fueldate'] # fueldate
        # shift = data['shift'] # Prel
        
        origin = request.POST.getlist('origin') # origin
        destination = request.POST.getlist('destination') # destination
        distances = request.POST.getlist('distance') # distance


        rider = request.POST.get('Pname','')
        date = request.POST.get('fueldate','') 
        shift = request.POST.get('Prel','') 
        

        total_distance = float(request.POST.get('Total_Distance')) # Total_Distance

        fuel_charges = float(request.POST.get('calfuel','')) 
        incentive = float(request.POST.get('incentive','')) 
        total_payable = float(request.POST.get('TAP',''))
        
 

        # print(f"Data: {data}")

        if date != '':
            # Define the format of your input string
            input_string = date
            input_format = "%Y-%m-%d"

            # Convert the string to a date object
            date_object = datetime.datetime.strptime(input_string, input_format).date()
        
        # Create category object for fuel expense
        category_obj = ExpenseCategory.objects.get(name ="Fuel expense")
        
        
        # create expense object
        exp =   Expense.objects.create(
                    amount = total_payable,
                    date = date_object,
                    description = rider,
                    category = category_obj,
                    created_by = request.user.username
                )

        # # create calculator object
        FuelCalculator.objects.create(
            rider_name = rider,
            fuel_date = date_object,
            shift = shift,
            total_distance = total_distance,
            fuel_charges = fuel_charges,
            incentive = incentive,
            amount_payable = total_payable,
            origin_array = origin,
            destination_array = destination,
            distances_array = distances,
            expense_obj = exp
        )

        # redirect to expense
        # if request.user.is_superuser:
        #     res = {"redirect_url": "http://127.0.0.1:8000/expense/view/"}
        # else:
        #     res = {"redirect_url": "http://127.0.0.1:8000/expense/expense_user/"}
        # res = {"message":"Expense Saved"}

        # return JsonResponse(
        #     res,
        #     safe=False
        # )
        if request.user.is_superuser:
            return redirect('expense')
        else:
            return redirect('expense_user')