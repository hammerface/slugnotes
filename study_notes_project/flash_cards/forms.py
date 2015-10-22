from django import forms
from .models import Deck, Card

class NewDeck(forms.ModelForm):

	class Meta:
		model = Deck
		fields = ("deck_name", "share_flag")
		labels = {
			'share_flag' : 'Share with others'
		}
