from django import forms
from .models import Bb, AdditionalImage, Client
from django.forms import inlineformset_factory
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

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

class ClientRegForm(forms.ModelForm):
	email = forms.EmailField(
		required = True,
		label = 'Электронная почта')
	pass1 = forms.CharField(
		label = 'Пароль',
		widget = forms.PasswordInput,
		help_text = password_validation.password_validators_help_text_html())
	pass2 = forms.CharField(
		label = 'Введите пароль повторно',
		widget = forms.PasswordInput,
		help_text = password_validation.password_validators_help_text_html())

	def clean(self):
		passw1 = self.cleaned_data['pass1']
		if passw1:
			password_validation.validate_password(passw1)
		super().clean()
		passw2 = self.cleaned_data['pass2']
		if passw1 and passw2 and passw1 != passw2:
			errors = {'pass2' : ValidationError(
				'Введенные пароли не совпадают',
				code = 'password_missmatch')}
			raise ValidationError(errors)

	def save(self, commit = True):
		user = super().save(commit = False)
		user.set_password(self.cleaned_data['pass1'])
		if commit:
			user.save()
		return user

	class Meta:
		model = Client
		fields = ('username', 'email', 'pass1', 'pass2', 'first_name', 'last_name')