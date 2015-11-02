from django.shortcuts import render
from flash_cards.forms import NewDeck, UploadFile
from django.http import HttpResponse, HttpResponseRedirect
import json
from flash_cards.models import Card, Deck
from django.core.signing import Signer
from django.core import signing


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

def View_Card(request):
	deck_id_signed = request.GET.get('deck_id')
	deck_id = None
	card_list =[]
	signer = Signer(request.user.id)
	try:
		deck_id = signer.unsign(deck_id_signed)
	except signing.BadSignature:
		print("Tampering detected!")
		return HttpResponseRedirect('/')
	cards = Card.objects.filter(deck_id=deck_id).order_by('-date_created')
	for card in cards:
		card_list.append({
			"card_id" : card.card_id,
			"front" : card.front,
			"back" : card.back,
			})
	context = {
		"card_list" : card_list,
	}
	

	return render(request, 'flash_cards/view_card.html', context)