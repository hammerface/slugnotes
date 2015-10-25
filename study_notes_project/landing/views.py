from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from flash_cards.models import Card, Deck
from flash_cards.forms import NewDeck
from django.http import HttpResponse, HttpResponseRedirect



# Create your views here.

def Home(request):
    form = None
    deck_list = []
    if request.user.is_authenticated:
        user_id = request.user.id
        #new deck form
        if request.method == "POST":
            form = NewDeck(request.POST)
            if form.is_valid():
                deck = form.save(commit=False)
                deck.user_id = user_id
                deck.save()
                return HttpResponseRedirect('/')
        else:
            form = NewDeck()
        #grab all decks associated with a user order by descending date created
        decks = Deck.objects.filter(user_id=user_id).order_by('-date_created')
        for deck in decks:
            deck_list.append({
                            "deck_id" : deck.deck_id, 
                            "deck_name" : deck.deck_name, 
                            "share" : deck.share_flag
                            })        

    context = {
        "form"      : form,
        "deck_list" : deck_list,
    }
    return render(request, "landing/home.html", context)