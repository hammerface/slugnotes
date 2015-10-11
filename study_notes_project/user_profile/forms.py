from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import SignUp


# class SignUpForm(forms.ModelForm):
# 	class Meta:
# 		model = SignUp
# 		fields = ['full_name', 'email']

# 	#validation methods
# 	def clean_email(self):
# 		#does default checks
# 		email = self.cleaned_data.get('email')
# 		email_base, provider = email.split("@")
# 		domain, extension = provider.split('.')
# 		#check .edu
# 		if not extension == "edu":
# 			raise forms.ValidationError("Please use valid .edu email address")
# 		return email

# 	def clean_full_name(self):
# 		full_name = self.cleaned_data.get('full_name')
# 		return full_name

class SignUpForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'email', 'first_name', 'last_name']

	def clean_username(self):
		username = self.cleaned_data.get('username')
		return username

# http://stackoverflow.com/questions/13202845/removing-help-text-from-django-usercreateform	
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username",  "password1", "password2", "email")
    # Check that username doesn't already exist
    def clean_username(self):
        username=self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('The username is already taken. Please try with another.')

    # Check for a valid .edu email accounts
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        if not extension == "edu":
            raise forms.ValidationError("Please use valid .edu email address.")
        return email

    # Check that passwords match
    def clean_password2(self):
    	password1 = self.cleaned_data.get('password1')
    	password2 = self.cleaned_data.get('password2')
    	if password1 != password2:
    		raise forms.ValidationError("Passwords don't match!")
    	return password2

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class UpdateProfile(UserCreateForm):
    email = forms.EmailField(required=False)