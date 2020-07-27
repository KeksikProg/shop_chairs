from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Bb
from .cart import Cart
from .forms import CartAddForm


@require_POST
def cart_add(request, product_id):
	cart = Cart(request) # Создаем или берем из сессии коризну
	product = get_object_or_404(Bb, pk = product_id) # пытаемя получить продукт
	form = CartAddForm(request.POST) # вы
	if form.is_valid():
		cd = form.cleaned_data
		cart.add_or_update(product = product,
			qua = cd['qua'],
			update_qua = cd['update'])
	return redirect('cart:cart_detail')


def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Bb, pk=product_id)
	cart.remove(product)
	return redirect('cart:cart_detail')