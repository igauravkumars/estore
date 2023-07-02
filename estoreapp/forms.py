from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

class UserRegisterForm(UserCreationForm):
	username = forms.CharField(label = 'Username', widget = forms.TextInput(attrs = {'class':'form-control'}))
	password1 = forms.CharField(label = 'Password',widget = forms.PasswordInput(attrs = {'class':'form-control'}))
	password2 = forms.CharField(label = 'Confirm Password',widget = forms.PasswordInput(attrs = {'class':'form-control'}))
	email = forms.CharField(required = True,label = 'Email',widget = forms.EmailInput(attrs = {'class':'form-control'}))

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class MyProfileForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['name', 'locality', 'city', 'zipcode', 'state']
		widgets = {'name':forms.TextInput(attrs = {'class':'form-control'}),
				   'locality':forms.TextInput(attrs = {'class':'form-control'}),
				   'city':forms.TextInput(attrs = {'class':'form-control'}),
 				   'state':forms.Select(attrs = {'class':'form-control'}),
				   'zipcode':forms.NumberInput(attrs = {'class':'form-control'})

		}




