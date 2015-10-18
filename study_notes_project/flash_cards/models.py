from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# fix the default value for deck_name
class Deck(models.Model):
	deck_id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User)
	deck_name = models.CharField(max_length=100, blank=False)
	share_flag = models.BooleanField(default=0)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	deleted_flag = models.BooleanField(default=0)

class Card(models.Model):
	card_id = models.AutoField(primary_key=True)
	deck = models.ForeignKey(Deck)
	front = models.CharField(max_length=1000)
	back = models.CharField(max_length=2000)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	deleted_flag = models.BooleanField(default=0)
