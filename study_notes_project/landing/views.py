from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

def Home(request):
    # form = SignUpForm();
    # context = {
    #     "form" : form
    # }
    return render(request, "landing/home.html", {})#context)