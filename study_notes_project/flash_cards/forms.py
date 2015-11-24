from django import forms
from .models import Deck, Card

class NewDeck(forms.ModelForm):

	#deck_name = forms.CharField(required=True)

	class Meta:
		model = Deck
		fields = ("user", "deck_name", "share_flag")
		labels = {
			'share_flag' : 'Share With Others'
		}
		widgets = {'user': forms.HiddenInput()}


	def clean_deck_name(self):
		user_id = self.cleaned_data['user']
		deck_name = self.cleaned_data['deck_name']
		total = None
	
		total = Deck.objects.filter(deck_name=deck_name, user_id=user_id, deleted_flag = 0)
		if not total:
			return deck_name
		if "deck_name" in self.changed_data:
			raise forms.ValidationError('You already have a deck with that name.')

class NewCard(forms.ModelForm):

	front = forms.CharField( required=True, max_length=1000, label="Front of Card", widget=forms.Textarea(attrs={'class':"form-control"}) )
	back = forms.CharField( required=False, max_length=2000, label="Back of Card", widget=forms.Textarea(attrs={'class':"form-control"}) )

	class Meta:
		model = Card
		fields = ("front", "back", "deck")
		widgets = {'deck': forms.HiddenInput()}

class UploadFile(forms.Form):
    file = forms.FileField(required=False)
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':13, 'cols':33}))
    deck_id = forms.CharField(widget = forms.HiddenInput())

    def clean(self):

        # Get the field values submitted
        cleaned_data = super(UploadFile, self).clean()
        file = cleaned_data.get('file')
        text = cleaned_data.get('text')
        if file == None and text == "":
			raise forms.ValidationError('Please fill out a field.')

        if file and text:
            raise forms.ValidationError('Only fill out one field please.', code='invalid')

        if file:
        	try:
	        	file, extension = str(file).split('.')
	        except ValueError:
	        	raise forms.ValidationError('The file has no extension, please use a .txt file')
	        if extension != 'txt':
	        	raise forms.ValidationError('Please select a .txt file')

