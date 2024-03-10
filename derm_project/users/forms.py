"""
forms for registration, updating email, 
username, bio, & the profile image.
password updating NOT handled here
(occurs in the background of the relevant HTML pages)
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
	"""
	UserRegisterForm
	"""
	email = forms.EmailField()

	class Meta:
		"""
		meta
		"""
		model = User
		# password1 and password2 must match
		fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	"""
	UserUpdateForm
	"""
	email = forms.EmailField()

	class Meta:
		"""
		meta
		"""
		model = User
		fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
	"""
	ProfileUpdateForm
	"""
	class Meta:
		"""
		meta
		"""
		model = Profile
		fields = ['bio', 'image']
