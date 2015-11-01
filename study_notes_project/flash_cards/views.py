from django.shortcuts import render
from flash_cards.forms import NewDeck
from django.http import HttpResponse, HttpResponseRedirect
import json
from flash_cards.models import Card, Deck

# Create your views here.
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



## using serialize
# from django.shortcuts import render
# from flash_cards.forms import NewDeck
# from django.http import HttpResponse, HttpResponseRedirect

# # Create your views here.
# def New_Deck(request):
# 	if request.method == 'POST':
# 		print "here" , request.POST.get('deck_name')
# 		data = {'user':'1','deck_name':"what are we?"}
# 		form = NewDeck(data)
# 		print request.POST
# 		if form.is_valid():
# 			print "Valid new deck"
# 		else:
# 			print "not valid"
# 		print "I AM HERE"
# 		# user = request.POST.get('user')
# 		# deck_name = request.POST.get('deck_name')
# 		# share_flag = request.POST.get('share_flag')

# 		# print user , deck_name , share_flag
# 	return HttpResponse("Inactive user.")