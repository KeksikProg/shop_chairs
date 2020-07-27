from django.shortcuts import render
from .models import Rubric, Bb, Client
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from .forms import OrderForm, AIFormSet
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.http import HttpResponse, Http404
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ChangeUserInfoForm, ClientRegForm
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from cart.forms import CartAddForm


def home(request):
	bbs = Bb.objects.all()[:10]
	cart_product_form = CartAddForm()
	context = {'bbs':bbs, 'cart_product_form':cart_product_form}
	return render(request, 'main/home.html', context)

class BbLogin(LoginView):
	template_name = 'main/login.html'


def other(request, page): # Это будет наша страница со скучными бумагами
	try:
		template = get_template('main/' + page + '.html') # Пытаемся получить шаблон
	except TemplateDoesNotExist: # Если не находит такуб страницу
		raise Http404 # То ошибка 404 (страница не найдена)
	return HttpResponse(template.render(request = request))

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

class ChangeUserInfo(UpdateView, LoginRequiredMixin, SuccessMessageMixin):
	model = Client
	template_name = 'main/change_user_info.html'
	form_class = ChangeUserInfoForm
	success_url = reverse_lazy('main:home')
	success_messsage = 'Личные данные пользователя были успешно изменены!'

	def dispatch(self, request, *args, **kwargs):
		self.user_id = request.user.pk
		return super().dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk = self.user_id)

class UserPasswordChange(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
	template_name = 'main/change_password.html'
	success_url = reverse_lazy('main:home')
	success_messsage = 'Пароль успешно изменен!'

class BbLogout(LogoutView, LoginRequiredMixin):
	template_name = 'main/logout.html'

class DeleteUserView(LoginRequiredMixin, DeleteView, SuccessMessageMixin):
	model = Client
	template_name = 'main/delete_user.html'
	success_url = reverse_lazy('main:home')

	def dispatch(self, request, *args, **kwargs):
		self.user_id = request.user.pk
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		logout(request)
		messages.add_message(request, messages.SUCCESS, message = 'Пользователь успешно удален!')
		return super().post(request, *args, **kwargs)

	def get_object(self, queryset=None):
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk = self.user_id)

class UserRegisterView(CreateView):
	model = Client
	template_name = 'main/register.html'
	form_class = ClientRegForm
	success_url = reverse_lazy('main:register_done')

class RegisterDoneView(TemplateView): # Это класс для вывода страницы о том что пользователь успешно создан и его нужно потвердить, а суперкласс чисто для вывода шаблона отрендеренного
	template_name = 'main/register_done.html'