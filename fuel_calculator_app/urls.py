from django.urls import path
from . import views
from . import api

    # path('fuel-expense-report', views.fuel_expense_report, name="fuel_expense_report"),
urlpatterns = [

    path('calculate-fuel/', views.calculate_fuel, name="calculate_fuel"),
    path('get-fuel/', api.get_fuel),
]
