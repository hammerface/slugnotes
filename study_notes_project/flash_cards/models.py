from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# fix the default value for deck_name
# don't allow the user to edit things they shouldn't use
SHARE_CHOICES = [(0,"No"), (1,"Yes")]
class Deck(models.Model):
	deck_id = models.AutoField(primary_key=True, editable=False)
	user = models.ForeignKey(User)
	deck_name = models.CharField(max_length=20, blank=False)
	share_flag = models.BooleanField(choices=SHARE_CHOICES, default=0)
	date_created = models.DateTimeField(auto_now_add=True, editable=False)
	date_modified = models.DateTimeField(auto_now=True, editable=False)
	deleted_flag = models.BooleanField(default=0, editable=False)

class Card(models.Model):
	card_id = models.AutoField(primary_key=True, editable=False)
	deck = models.ForeignKey(Deck)
	front = models.CharField(max_length=1000)
	back = models.CharField(max_length=2000)
	date_created = models.DateTimeField(auto_now_add=True, editable=False)
	date_modified = models.DateTimeField(auto_now=True, editable=False)
	deleted_flag = models.BooleanField(default=0, editable=False)
