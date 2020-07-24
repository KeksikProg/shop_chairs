from django import forms
from .models import Bb, AdditionalImage, Client
from django.forms import inlineformset_factory

class OrderForm(forms.ModelForm):
	class Meta:
		model = Bb
		fields = '__all__'

AIFormSet = inlineformset_factory(Bb, AdditionalImage, fields = '__all__')

class ChangeUserInfoForm(forms.ModelForm):
	email = forms.EmailField(required = True, label = 'Адрес электронной почты')

	class Meta:
		model = Client
		fields = ('username', 'email', 'first_name', 'last_name')