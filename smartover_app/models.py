from django.db import models
from django.utils.timezone import localtime
from user_profile.models import UserProfile
from django.contrib.auth.models import User

# Create your models here.



class Task(models.Model):
	creation_date = models.DateTimeField(default=localtime)
	description = models.TextField()
	created_by = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
	closing_date =  models.DateTimeField(null=True, blank=True)
	closed_by = models.OneToOneField(to=UserProfile)
	remarks = models.TextField()



# Rest of the work is pending