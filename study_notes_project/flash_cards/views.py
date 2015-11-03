from django.shortcuts import render
from flash_cards.forms import NewDeck, UploadFile, NewCard
from django.http import HttpResponse, HttpResponseRedirect
import json
from flash_cards.models import Card, Deck
from django.core.signing import Signer
from django.core import signing
from django.shortcuts import get_object_or_404


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

def Edit_Deck(request):
        deck_id_signed = request.GET.get('deck_id')
	deck_id = None
	signer = Signer(request.user.id)
	try:
		deck_id = signer.unsign(deck_id_signed)
	except signing.BadSignature:
		print("Tampering detected!")
		return HttpResponseRedirect('/')
        deck = get_object_or_404(Deck, deck_id=deck_id)
	deck.deck_name = "NewDeck"
        deck.share_flag = 1
        deck.save()
	return HttpResponseRedirect('/')

def Delete_Deck(request):
        deck_id_signed = request.GET.get('deck_id')
	deck_id = None
	signer = Signer(request.user.id)
	try:
		deck_id = signer.unsign(deck_id_signed)
	except signing.BadSignature:
		print("Tampering detected!")
		return HttpResponseRedirect('/')
        deck = get_object_or_404(Deck, deck_id=deck_id)
        deck.deleted_flag = 1
        deck.save()
	return HttpResponseRedirect('/')

def Upload_File(request):
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
        	content = None
        	if request.POST.get('text', False) != False:
        		content = request.POST['text']
        	if request.FILES.get('file', False) != False:
        		content = request.FILES['file']
        		content = content.read()
        	return HttpResponseRedirect('/')
    else:
        form = UploadFile()
    return render(request, 'landing/upload.html', {'form': form})

def View_Deck(request):

	deck_id_signed = request.GET.get('deck_id')
	deck_id = None
	card_list =[]
	signer = Signer(request.user.id)
	try:
		deck_id = signer.unsign(deck_id_signed)
	except signing.BadSignature:
		print("Tampering detected!")
		return HttpResponseRedirect('/')
	form = NewCard(initial={'deck' : request.GET.get('deck_id')})
	cards = Card.objects.filter(deck_id=deck_id).order_by('-date_created')
	for card in cards:
		card_list.append({
			"card_id" : card.card_id,
			"front" : card.front,
			"back" : card.back,
			})
	context = {
		"form" : form,
		"card_list" : card_list,
	}
	return render(request, 'flash_cards/view_deck.html', context)

def New_Card(request):
	if request.method == 'POST':
		deck = request.POST.get('deck')
		front = request.POST.get('front')
		back = request.POST.get('back')
		signer = Signer(request.user.id)
		try:
			deck = signer.unsign(deck)
		except signing.BadSignature:
			return HttpResponseRedirect('/')
		data = {'deck' : deck, 'front' : front, 'back' : back}		
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

def Delete_Card(request):
        card_id = request.GET.get('card_id')
	#card_id = card.card_id
	#signer = Signer(request.user.id)
	#try:
        #card_id = signer.unsign(card_id_signed)
	#except signing.BadSignature:
	#	print("Tampering detected!")
	#	return HttpResponseRedirect('/')
        card = get_object_or_404(Card, card_id=card_id)
        card.deleted_flag = 1
        card.save()
	return HttpResponseRedirect('/')
