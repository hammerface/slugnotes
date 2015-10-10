from django.db import models
#from django.contrib.auth.model import User
# Create your models here.
# class SignUp(models.Model):
# 	email 		= models.EmailField();
# 	full_name 	= models.CharField(max_length=120);
# 	timestamp 	= models.DateTimeField(auto_now_add=True, auto_now=False);
# 	#Auto_now_add only change on the first time entered, auto_now changes on saved/updated

# 	#needed
# 	def __unicode__(self):
# 		# main thing returned could use return self.email
# 		return self.full_name
# class SignUp(models.Model):
# 	user = models.OneToOneField(User)