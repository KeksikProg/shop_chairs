from django import forms

product_qua = [(i, str(i)) for i in range (1, 21)] 
# выше это наш виджет который позволит клиенту заказывать товар максимум в кол-во 20 штук и не более

class CartAddForm(forms.Form):
	qua = forms.TypedChoiceField(choices = product_qua, coerce = int)
	update = forms.BooleanField(required = False, initial = False, widget=forms.HiddenInput)