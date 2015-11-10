from django.shortcuts import render
from flash_cards.forms import NewDeck, UploadFile, NewCard
from django.http import HttpResponse, HttpResponseRedirect
import json
from flash_cards.models import Card, Deck
from django.core.signing import Signer
from django.core import signing
from django.shortcuts import get_object_or_404
from parse_notes import parse_notes
import re
from django.contrib.auth.models import User
from django.db.models import Q


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
    		print("Tampering detected!!")
    		return HttpResponseRedirect('/')
        deck_name = request.POST.get('deck_name')
        user = request.POST.get('user')
        share_flag = request.POST.get('share_flag')
        if share_flag == 'false':
            share_flag = 0
        else:
            share_flag = 1
        data = {'user' : user, 'deck_name' : deck_name, "share_flag" : share_flag}
        deck = get_object_or_404(Deck, deck_id=deck_id)
        if deck.deck_name == deck_name:
            deck.share_flag = share_flag
            deck.save()
        else:
            form = NewDeck(data)
            if form.is_valid():

                #deck = get_object_or_404(Deck, deck_id=deck_id)
                deck.deck_name = deck_name
                deck.share_flag = share_flag
                deck.save()
            else:
                errors = form.errors
                return HttpResponse(json.dumps(errors))
    
    return HttpResponse(json.dumps({"success": "success"}))

def Delete_Deck(request):
    deck_id_signed = request.POST.get('deck')
    deck_id = None
    signer = Signer(request.user.id)
    try:
        deck_id = signer.unsign(deck_id_signed)
    except signing.BadSignature:
        print("Tampering detected! Delete deck")
        return HttpResponse(json.dumps(errors))
    deck = get_object_or_404(Deck, deck_id=deck_id)
    deck.deleted_flag = 1
    deck.save()
    return HttpResponse(json.dumps({"success": "success"}))

def Upload_File(request):
    signer = Signer(request.user.id)
    deck_id_signed = request.GET.get('deck_id')
    deck_id = None
    try:
        deck_id = signer.unsign(request.GET.get('deck_id'))
    except signing.BadSignature:
        print("Tampering detected! Upload file")
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
                back = ""
                #loop through card list and generate a new card for the deck
                for card in cardslist:
                    if len(card) > 1:
                        front = card.pop(0)
                        for line in card:
                            print line
                            back += re.sub(r'\r', '', line) + "\n"
                    else:
                        front = card.pop(0)
                    new_card = Card.objects.create(deck_id = deck_id, front=front,back=back)
                    back = ""
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
        print("Tampering detected! View deck")
        return HttpResponseRedirect('/')
    form = NewCard(initial={'deck' : request.GET.get('deck_id')})
    cards = Card.objects.filter(deck_id=deck_id, deleted_flag = 0).order_by('-date_created')
    deck = Deck.objects.filter(deck_id=deck_id)
    print "here"
    deck_name = ""
    try:
        deck_name = deck[0].deck_name
    except IndexError:
        deck_name = ""
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
        "deck_name" : deck_name, 
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
        card_id = request.POST.get('card')
        deck_id_signed = request.POST.get('deck')
        deck_id = None
	signer = Signer(request.user.id)
	try:
                deck = signer.unsign(deck_id_signed)
	except signing.BadSignature:
		print("Tampering detected! Delete card")
		return HttpResponse(json.dumps(errors))
        card = get_object_or_404(Card, card_id=card_id)
        card.deleted_flag = 1
        card.save()
	return HttpResponse(json.dumps({"success": "success"}))


def Search(request):
    query = request.GET.get('query')
    users = User.objects.filter(username__contains=str(query))
    user_list = []
    signer = Signer(request.user.id)
    #SQL SELECT * FROM flash_cards_deck where deck_name like '%hello%' and deleted_flag = 0 and share_flag = 1
    decks = Deck.objects.filter(deck_name__contains=str(query), share_flag = 1, deleted_flag = 0).exclude(user_id=request.user.id)
    deck_list = []
    for user in users:
        public_deck_count = Deck.objects.filter(user_id = user.id, share_flag = 1).count()
        user_list.append({
            "user" : user.id,
            "username" : user.username,
            "public_deck_count" : public_deck_count,
            })
    for deck in decks:
        print deck.deck_id
        deck_list.append({
            "orig_deck_id" : signer.sign(deck.deck_id),
            "deck_name" : deck.deck_name,
            "share" : deck.share_flag,
            })
    form = NewDeck(initial={'user' : request.user.id})
    context = {
        "user_list" : user_list,
        "deck_list" : deck_list,
        "clone_form" : form,
        "sign" : signer.sign(request.user.id),
    }
    return render(request, 'flash_cards/search.html', context)

def Shared_Decks(request):
    u_id = request.GET.get('u_id')
    shared_decks = Deck.objects.filter(user_id = u_id, share_flag = 1)
    form = NewDeck(initial={'user' : request.user.id})
    context = {
        "shared_user_id" : u_id,
        "shared_decks" : shared_decks,
        "clone_form" : form,
    }
    return render(request, 'flash_cards/shared_profile.html', context)

def Clone(request):
    if request.method == 'POST':
        signer = Signer(request.user.id)

        user = request.POST.get('user')
        deck_name = request.POST.get('deck_name')
        share_flag = request.POST.get('share_flag')
        clone_deck_id = request.POST.get('clone_deck_id')
        try:
            user = signer.unsign(user)
            clone_deck_id = signer.unsign(clone_deck_id)
        except signing.BadSignature:
            return HttpResponse(json.dumps({"Tampering": "bad signature"}))
        if share_flag == 'false':
            share_flag = 0
        else:
            share_flag = 1
        data = {'user' : user, 'deck_name' : deck_name, 'share_flag' : share_flag}
        #create the new deck
        form = NewDeck(data)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.user_id = user
            deck.save()
            new_deck_id = deck.deck_id
            #add all the cards from the shared deck to your new deck
            cards = Card.objects.filter(deck_id = clone_deck_id, deleted_flag = 0)
            for card in cards:
                new_card = Card.objects.create(deck_id = new_deck_id, front=card.front,back=card.back)

        else:
            print "error"
            errors = form.errors
            print errors
            return HttpResponse(json.dumps(errors))

    return HttpResponse(json.dumps({"success": "success"}))
