from django import forms
from .models import Bb, AdditionalImage
from django.forms import inlineformset_factory

class OrderForm(forms.ModelForm):
	class Meta:
		model = Bb
		fields = '__all__'

AIFormSet = inlineformset_factory(Bb, AdditionalImage, fields = '__all__')