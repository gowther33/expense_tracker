from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from cloudinary.models import CloudinaryField


def user_path(instance, filename):
	
	path = 'profile_pic/{0}-{1}/{2}'.format(instance.user.username ,instance.user.id,filename)
	return path


class UserProfile(models.Model):
	user = models.OneToOneField(to = User,on_delete = models.CASCADE)

	profile_pic = models.ImageField(blank=True,upload_to=user_path)

	email_preference = models.BooleanField(default=True)
	created_at = models.DateTimeField(default=localtime)

	def __str__(self):
		return str(self.user) + 's' + 'profile' 