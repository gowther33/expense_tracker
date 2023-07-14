from django.db import models
# from django.contrib.auth.models import User
from django.utils.timezone import localtime
from income_app.models import Income


# user = models.ForeignKey(to = User,on_delete=models.CASCADE)
# dues are related to income
class Due(models.Model):
	amount = models.FloatField()
	date = models.DateField(default=localtime)
	description = models.TextField()
	source = models.OneToOneField(
		to = Income,
		on_delete=models.CASCADE
	)
	created_at = models.DateTimeField(default=localtime)
	received_at = models.DateTimeField(null=True, blank=True)


	def __str__(self):
		return str(self.source) + str(self.date )+ str(self.amount)


"""
to change:
import dues functionality
and download

searching.js for dues
sorting.js for dues

income_count id 

"""