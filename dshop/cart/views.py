from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Bb
from .cart import Cart
from .forms import CartAddForm

def cart_detail(request):
	cart = Cart(request)
	context = {'cart':cart}
	return render(request, 'cart/detail.html', context)


# Create your views here.
