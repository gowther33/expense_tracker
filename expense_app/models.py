from django.db import models
# from django.contrib.auth.models import User
from django.utils.timezone import localtime


# user = models.ForeignKey(to = User,on_delete=models.CASCADE)
class ExpenseCategory(models.Model):
	name = models.CharField(max_length = 256)
	created_at = models.DateTimeField(default=localtime)
	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Expense Categories'

# user = models.ForeignKey(to = User,on_delete=models.CASCADE)
class Expense(models.Model):
	amount = models.FloatField()
	date = models.DateField(default=localtime)
	description = models.TextField()
	category = models.ForeignKey(to=ExpenseCategory,on_delete=models.CASCADE)
	created_at = models.DateTimeField(default=localtime)
	created_by = models.TextField()

	def __str__(self):
		return str(self.category) + str(self.date )+ str(self.amount)

