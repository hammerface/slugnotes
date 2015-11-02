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
	
		total = Deck.objects.filter(deck_name=deck_name, user_id=user_id)
		if not total:
			return deck_name
		if "deck_name" in self.changed_data:
			raise forms.ValidationError('You already have a deck with that name.')

class UploadFile(forms.Form):
    file = forms.FileField(required=False)
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':13, 'cols':33}))

    def clean(self):

        # Get the field values submitted
        cleaned_data = super(UploadFile, self).clean()
        file = cleaned_data.get('file')
        text = cleaned_data.get('text')
        if file:
	        f = str(file).split('.')
	    	if f[1] != 'txt':
	    		raise forms.ValidationError('Please select a .txt file.')
        if file and text:
            raise forms.ValidationError('Only fill out one field please.', code='invalid')




    # def check_fields(self):
    # 	print self.cleaned_data['text']
    # 	print self.cleaned_data['file']
    # 	return 

