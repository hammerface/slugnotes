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
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('The email is already in use. Please try another')

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

class UpdateProfile(forms.ModelForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    # Check that username doesn't already exist
    # http://stackoverflow.com/questions/23361057/django-comparing-old-and-new-field-value-before-saving
    def clean_username(self):
        username=self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        if "username" in self.changed_data:
            raise forms.ValidationError('The username is already taken. Please try with another.')


    # Check for a valid .edu email accounts
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        if not extension == "edu":
            raise forms.ValidationError("Please use valid .edu email address.")
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('The email is already in use. Please try another')


class ChangePassword(UserCreationForm):
    old_password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("password1", "password2")

    #def clean_password(self):


# https://github.com/django/django/blob/master/django/contrib/auth/forms.py
# class SetPasswordForm(forms.Form):
#     """
#     A form that lets a user change set their password without entering the old
#     password
#     """
#     error_messages = {
#         'password_mismatch': "The two password fields didn't match.",
#     }
#     new_password1 = forms.CharField(label="New password",
#                                     widget=forms.PasswordInput,
#                                     )
#     new_password2 = forms.CharField(label="New password confirmation",
#                                     widget=forms.PasswordInput)

#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super(SetPasswordForm, self).__init__(*args, **kwargs)

#     def clean_new_password2(self):
#         password1 = self.cleaned_data.get('new_password1')
#         password2 = self.cleaned_data.get('new_password2')
#         if password1 and password2:
#             if password1 != password2:
#                 raise forms.ValidationError(
#                     self.error_messages['password_mismatch'],
#                     code='password_mismatch',
#                 )
#         password_validation.validate_password(password2, self.user)
#         return password2

#     def save(self, commit=True):
#         password = self.cleaned_data["new_password1"]
#         self.user.set_password(password)
#         if commit:
#             self.user.save()
#         return self.user


# class PasswordChangeForm(SetPasswordForm):
#     """
#     A form that lets a user change their password by entering their old
#     password.
#     """
#     error_messages = dict(SetPasswordForm.error_messages, **{
#         'password_incorrect': "Your old password was entered incorrectly. "
#                                 "Please enter it again.",
#     })
#     old_password = forms.CharField(label="Old password",
#                                    widget=forms.PasswordInput)

#     field_order = ['old_password', 'new_password1', 'new_password2']

#     def clean_old_password(self):
#         """
#         Validates that the old_password field is correct.
#         """
#         old_password = self.cleaned_data["old_password"]
#         if not self.user.check_password(old_password):
#             raise forms.ValidationError(
#                 self.error_messages['password_incorrect'],
#                 code='password_incorrect',
#             )
#         return old_password
