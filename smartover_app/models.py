from django.db import models
from django.utils.timezone import localtime
from django.contrib.auth.models import User

# Create your models here.

"""
1 = LOW
2 = MEDIUM
3 = HIGH
4 = CRITICAL
"""


class Task(models.Model):

	date = models.DateTimeField(default=localtime) # Creation date
	description = models.TextField()
	created_by = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="task_initiator")
	closing_date =  models.DateTimeField(null=True, blank=True)
	# Null initially
	closed_by = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="task_closer", null=True, blank=True)
	remarks = models.TextField()
	priority = models.PositiveIntegerField(default=1)
	status = models.CharField(max_length=100, default="Open")


# Rest of the work is pending
# working for admin
# for user pending
