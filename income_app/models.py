from django.db import models
# from django.contrib.auth.models import User
from django.utils.timezone import localtime


	# user = models.ForeignKey(to = User,on_delete=models.CASCADE)
class IncomeSource(models.Model):
	source = models.CharField(max_length = 256)
	created_at = models.DateTimeField(default=localtime)
	def __str__(self):
		return self.source

	class Meta:
		verbose_name_plural = 'Income Sources'

	# user = models.ForeignKey(to = User,on_delete=models.CASCADE)
class Income(models.Model):
	amount = models.FloatField()
	date = models.DateField(default=localtime)
	description = models.TextField()
	source = models.ForeignKey(to=IncomeSource,on_delete=models.CASCADE)
	created_at = models.DateTimeField(default=localtime)
	created_by = models.TextField()

	def __str__(self):
		return str(self.source) + str(self.date )+ str(self.amount)
