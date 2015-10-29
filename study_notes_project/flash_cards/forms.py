from django import forms
from .models import Deck, Card

class NewDeck(forms.ModelForm):

	class Meta:
		model = Deck
		fields = ("user", "deck_name", "share_flag")
		labels = {
			'share_flag' : 'Share with others'
		}
		widgets = {'user': forms.HiddenInput()}
	def clean_deck_name(self):
		user_id = self.cleaned_data['user']
		deck_name = self.cleaned_data['deck_name']
		print deck_name
		if len(deck_name) > 32:
			raise forms.ValidationError('Exceeds max character length of 32.')
		total = None
	
		total = Deck.objects.filter(deck_name=deck_name, user_id=user_id)
		if not total:
			return deck_name
		if "deck_name" in self.changed_data:
			raise forms.ValidationError('You already have a deck with that name.')
