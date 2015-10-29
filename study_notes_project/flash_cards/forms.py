from django import forms
from .models import Deck, Card

class NewDeck(forms.ModelForm):
	deck_name = forms.CharField(required=True)

	class Meta:
		model = Deck
		fields = ("deck_name", "share_flag")
		labels = {
			'share_flag' : 'Share With Others'
		}


