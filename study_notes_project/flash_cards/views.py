from django.shortcuts import render
from flash_cards.forms import NewDeck, UploadFile, NewCard
from django.http import HttpResponse, HttpResponseRedirect
import json
from flash_cards.models import Card, Deck
from django.core.signing import Signer
from django.core import signing
from django.shortcuts import get_object_or_404
from parse_notes import parse_notes


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
    if request.method == 'POST':
        deck_id_signed = request.POST.get('deck_id')
        deck_id = None
        signer = Signer(request.user.id)
        try:
        	deck_id = signer.unsign(deck_id_signed)
        except signing.BadSignature:
    		print("Tampering detected!")
    		return HttpResponseRedirect('/')
        deck_name = request.POST.get('deck_name')
        user = request.POST.get('user')
        share_flag = request.POST.get('share_flag')
        if share_flag == 'false':
            share_flag = 0
        else:
            share_flag = 1
        data = {'user' : user, 'deck_name' : deck_name, "share_flag" : share_flag}
        form = NewDeck(data)
        if form.is_valid():

            deck = get_object_or_404(Deck, deck_id=deck_id)
            deck.deck_name = deck_name
            deck.share_flag = share_flag
            deck.save()
        else:
            errors = form.errors
            return HttpResponse(json.dumps(errors))
    
    return HttpResponse(json.dumps({"success": "success"}))

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
    signer = Signer(request.user.id)
    deck_id_signed = request.GET.get('deck_id')
    deck_id = None
    try:
        deck_id = signer.unsign(request.GET.get('deck_id'))
    except signing.BadSignature:
        print("Tampering detected!")
        return HttpResponseRedirect('/')

    #Notes have been uploaded to parser
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            deck_id = form.cleaned_data.get('deck_id')
            content = None
            if request.POST.get('text', False) != False:
                content = request.POST['text']
            if request.FILES.get('file', False) != False:
                content = request.FILES['file']
                content = content.read()
            cardslist = parse_notes(content)
            #check that there are any cards to create
            if cardslist:
                front = None
                back = None
                #loop through card list and generate a new card for the deck
                for card in cardslist:
                    front = card[0]
                    try: 
                        back = card[1]
                    except IndexError:
                        back = ""
                    new_card = Card.objects.create(deck_id = deck_id, front=front,back=back)
            return HttpResponseRedirect('/cards/?deck_id=' + str(deck_id_signed))
    else:
        form = UploadFile(initial={"deck_id" : deck_id})
    context = {
        "form" : form,
    }
    return render(request, 'landing/upload.html', context)

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
	cards = Card.objects.filter(deck_id=deck_id, deleted_flag = 0).order_by('-date_created')
	for card in cards:
		card_list.append({
			"card_id" : card.card_id,
			"front" : card.front,
			"back" : card.back,
			})
	context = {
		"form" : form,
		"card_list" : card_list,
        "deck_id" : deck_id_signed,
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

def Edit_Card(request):
        if request.method == 'POST':
                id_card = request.POST.get('card')
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
                print "%s" % id_card
                if form.is_valid():
                        card = get_object_or_404(Card, card_id=id_card)
                        card.front = front
                        card.back = back
                        card.save()
                else:
                        errors = form.errors
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
