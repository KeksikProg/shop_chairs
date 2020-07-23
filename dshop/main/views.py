from django.shortcuts import render
from .models import Rubric, Bb
from django.contrib.auth.views import LoginView
from .forms import OrderForm, AIFormSet
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages


def home(request):
	bbs = Bb.objects.all()[:10]
	context = {'bbs':bbs}
	return render(request, 'main/home.html', context)

class BbLogin(LoginView):
	template_name = 'main/login.html'

def add_order(request):
	if request.user.is_superuser:
		if request.method == 'POST':
			form = OrderForm(request.POST, request.FILES)
			if form.is_valid():
				order = form.save()
				formset = AIFormSet(request.POST, request.FILES, instance = order)
				if formset.is_valid():
					formset.save()
					messages.add_message(request, messages.SUCCESS, message = 'Товар успешно добавлен')
					return redirect ('main:home')
		else:
			form = OrderForm(initial = {})
			formset = AIFormSet()
		context = {'form' : form, 'formset' : formset}
		return render (request, 'main/add_order.html', context)
	else:
		raise Http404

def order_change(request, pk):
	if request.user.is_superuser:
		order = get_object_or_404(Bb, pk = pk)
		if request.method == 'POST':
			form = OrderForm(request.POST, request.FILES, instance = order)
			if form.is_valid():
				order = form.save()
				formset = AIFormSet(request.POST, request.FILES, instance = order)
				if formset.is_valid():
					formset.save()
					messages.add_message(request, messages.SUCCESS, message = 'Товар изменен')
					return redirect('main:home')
		else:
			form = OrderForm(instance = order)
			formset = AIFormSet(instance = order)
		context = {'form' : form, 'formset' : formset}
		return render(request, 'main/order_change.html', context)
	else:
		raise Http404

def order_delete(request, pk):
	if request.user.is_superuser:
		post = get_object_or_404(Bb, pk = pk)
		if request.method == 'POST':
			post.delete()
			messages.add_message(request, messages.SUCCESS, message = 'Товар удален')
			return redirect('main:home')
		else:
			context = {'post' : post}
			return render(request, 'main/order_delete.html', context)
	else:
		raise Http404

# Create your views here.
