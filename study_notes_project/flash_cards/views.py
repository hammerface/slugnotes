from django.shortcuts import render
from flash_cards.forms import NewDeck, UploadFile, NewCard
from django.http import HttpResponse, HttpResponseRedirect
import json
from flash_cards.models import Card, Deck

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

def View_Deck(request):
	print request.GET.get('deck_id')
	form = NewCard(initial={'deck' : request.GET.get('deck_id')})
	context = {
		"form" : form
	}
	return render(request, 'flash_cards/view_deck.html', context)

def New_Card(request):
	print "I am here"
	if request.method == 'POST':
		deck = request.POST.get('deck')
		front = request.POST.get('front')
		back = request.POST.get('back')
		data = {'deck' : deck, 'front' : front, 'back' : back}
		print data , "here"
		
		form = NewCard(data)
		if form.is_valid():
			print "valid form"
			card = form.save(commit=False)
			card.deck_id = deck
			card.save()
		else:
			print "error"
			errors = form.errors
			print errors
			return HttpResponse(json.dumps(errors))

	return HttpResponse(json.dumps({"success": "success"}))
