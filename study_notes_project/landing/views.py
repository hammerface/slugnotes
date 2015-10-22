from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from flash_cards.models import Card, Deck
from flash_cards.forms import NewDeck
from django.http import HttpResponse, HttpResponseRedirect



# Create your views here.

def Home(request):
    form = None
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NewDeck(request.POST)
            if form.is_valid():
                deck = form.save(commit=False)
                deck.user_id = request.user.id
                deck.save()
                return HttpResponseRedirect('/')
        else:
            form = NewDeck()
    context = {
        "form" : form,
    }
    return render(request, "landing/home.html", context)