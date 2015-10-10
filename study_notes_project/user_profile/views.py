from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from study_notes_project import settings
from .forms import UserCreateForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


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
            #invalid login
            #https://docs.djangoproject.com/en/dev/topics/auth/default/#user-objects
            messages.error(request, "Invalid username/password")
            return HttpResponseRedirect(settings.LOGIN_URL)
            

    return render(request, "user_profile/login.html", {})


# Home page requires sign in before getting here
@login_required
def Home(request):
    form = SignUpForm();
    context = {
        "form" : form
    }
    return render(request, "user_profile/home.html", context)

# The logout function, just logsout a user
def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


#http://stackoverflow.com/questions/21126005/how-to-get-django-view-to-return-form-errors
# Sign Up a new user by processing the UserCreateForm
def Signup(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            #add the user to the database
            return HttpResponseRedirect('/')
        # username = request.POST['username']
        # password1 = request.POST['password1']
        # password2 = request.POST['password2']
        # email = request.POST['email']
    else:
        form = UserCreateForm()
    context = {
        "form" : form,
    }
    return render(request,"user_profile/signup.html", context)


