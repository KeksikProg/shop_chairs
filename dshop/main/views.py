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
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView

'''Тут будут вьюхи связанные с товаром'''
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



'''Тут свьюхи домашняя и с дополнительной инфой'''

def home(request):
	bbs = Bb.objects.all()[:10]
	cart_product_form = CartAddForm()
	context = {'bbs':bbs, 'cart_product_form':cart_product_form}
	return render(request, 'main/home.html', context)


def other(request, page): # Это будет наша страница со скучными бумагами
	try:
		template = get_template('main/' + page + '.html') # Пытаемся получить шаблон
	except TemplateDoesNotExist: # Если не находит такуб страницу
		raise Http404 # То ошибка 404 (страница не найдена)
	return HttpResponse(template.render(request = request))



'''Тут вьюхи с входом, выходом и удалением пользователя'''

class BbLogin(LoginView):
	template_name = 'main/login.html'

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


'''Тут вьюхи с регистрацией и активацией'''

class UserRegisterView(CreateView):
	model = Client
	template_name = 'main/register.html'
	form_class = ClientRegForm
	success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView): # Это класс для вывода страницы о том что пользователь успешно создан и его нужно потвердить, а суперкласс чисто для вывода шаблона отрендеренного
	template_name = 'main/register_done.html'


from django.core.signing import Signer
signer = Signer()
def user_activate(request, sign):
	try:
		username = signer.unsign(sign)
	except BadSignature:
		raise Http404
	user = get_object_or_404(Client, username = username)
	if user.is_active:
		template = 'main/user_is_activated.html'
	else:
		template = 'main/activation_done.html'
		user.is_active = True
		user.save()
	return render(request, template)



'''Тут будут вьюхи с сбросом пароля'''

class ClientPasswordResetView(PasswordResetView):
	template_name = 'main/password_reset.html'
	subject_template_name = 'email/password_reset_subj.txt'
	email_template_name = 'email/password_reset_body.html'
	success_url = reverse_lazy('main:password_reset_done')


class ClientPasswordResetDone(PasswordResetDoneView):
	template_name = 'main/password_reset_done.html'

class ClientPasswordConfirmView(PasswordResetConfirmView):
	template_name = 'main/password_reset_confirm.html'
	success_url = reverse_lazy('main:login')

