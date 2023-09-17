from django.db import models
import datetime
from expense_app.models import Expense
# Create your models here.



class Fuel(models.Model):
    fuel_rate = models.DecimalField(max_digits=5, decimal_places=2)
    maintenance_factor = models.DecimalField(max_digits=5, decimal_places=2, default=1.5)
    idling_factor = models.DecimalField(max_digits=5, decimal_places=2, default=1.1)


class FuelCalculator(models.Model):
    rider_name = models.CharField(max_length=100) # Pname
    fuel_date = models.DateField(default=datetime.date.today)
    shift = models.CharField(max_length=10) # Prel: Morning Evening

    total_distance = models.FloatField() # Psum 

    fuel_charges = models.DecimalField(
        max_digits=5,
        decimal_places=2
    ) # calfuel
    incentive = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    ) # Maintenance
    amount_payable = models.FloatField() # TAP
    
    origin_array = models.JSONField()
    destination_array = models.JSONField()
    distances_array = models.JSONField()
    expense_obj = models.OneToOneField(to=Expense, on_delete=models.CASCADE) 
    

    