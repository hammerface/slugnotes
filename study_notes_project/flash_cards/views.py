from django.shortcuts import render
from flash_cards.forms import NewDeck, UploadFile
from django.http import HttpResponse, HttpResponseRedirect
import json
from flash_cards.models import Card, Deck
import os

def New_Deck(request):
	if request.method == 'POST':
		user = request.POST.get('user')
		deck_name = request.POST.get('deck_name')
		share_flag = request.POST.get('share_flag')
		if share_flag == 'false':
			share_flag = 0
		else:
			share_flag = 1
		data = {'user' : user, 'deck_name' : deck_name, 'share_flag' : share_flag}
		
		form = NewDeck(data)
		if form.is_valid():
			print "valid form"
			deck = form.save(commit=False)
			deck.user_id = user
			deck.save()
		else:
			print "error"
			errors = form.errors
			print errors
			return HttpResponse(json.dumps(errors))

	return HttpResponse(json.dumps({"success": "success"}))

def Upload_File(request):
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            temp_file = request.FILES['file']
            return HttpResponseRedirect('/')
    else:
        form = UploadFile()
    return render(request, 'landing/upload.html', {'form': form})
