from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from study_notes_project import settings
from .forms import UserCreateForm, SignUpForm, UpdateProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User

# more

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
            new_user = User.objects.create_user(username = form.cleaned_data.get('username'), 
                email= form.cleaned_data.get('email'), password= form.cleaned_data.get('password1'), 
                first_name = form.cleaned_data.get('first_name'), last_name= form.cleaned_data.get('last_name'))
            return HttpResponseRedirect('/')
    else:
        form = UserCreateForm()
    context = {
        "form" : form,
    }
    return render(request,"user_profile/signup.html", context)

# Editable Profile page
@login_required
def Profile(request):
    #user = User.objects.get(username='testing2').first_name
    # username = None
    # form = None
    # username = request.user.username
    # user = User.objects.get(username=username)
    # username = user.username
    # first_name = user.first_name
    # last_name = user.last_name
    # email = user.email
    if request.method == "POST":
        form = UpdateProfile(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponseRedirect('/')
    else:
        form = UpdateProfile(instance=request.user)
    context = {
        "form" : form
    }
    #print username , first_name, last_name, email
    #print user
    return render(request,"user_profile/profile.html",context)


