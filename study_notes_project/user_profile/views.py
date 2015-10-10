from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from study_notes_project import settings


def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
            

    return render(request, "user_profile/login.html", {})

@login_required
def Home(request):
    return render(request, "user_profile/home.html", {})

def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)






