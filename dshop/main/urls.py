from django.urls import path 
from .views import home
from .views import BbLogin, add_order,order_delete,order_change, other, ChangeUserInfo, UserPasswordChange, BbLogout
from .views import DeleteUserView, UserRegisterView, RegisterDoneView, user_activate

app_name = 'main'

urlpatterns = [

	# ТУт у нас начальная страница и страница для дополнительной информации
	path('', home, name = 'home'), # Начальная страница
	path('other/<str:page>/', other, name = 'other'), # Страница с дополнитульной инофрмацией
	
	#Тут у нас все что связано с пользователем и его профилем
	path('profile/login/', BbLogin.as_view(), name = 'login'), # страница входа
	path('profile/change_info', ChangeUserInfo.as_view(), name = 'change_info'), # страница смены информации о пользователе
	path('profile/change_pass', UserPasswordChange.as_view(), name = 'change_pass'), # страница смены пароля
	path('profile/logout', BbLogout.as_view(), name = 'logout'), # страница выхода
	path('profile/delete_user', DeleteUserView.as_view(), name = 'delete_user'), # страница удаления пользователя
	path('profile/register_user', UserRegisterView.as_view(), name = 'user_register'), # страница регистрации
	path('profile/register_done', RegisterDoneView.as_view(), name = 'register_done'), # страница на которой говорится что для потверждения пользователя надо зайти на почту и потвердить его
	path('profile/register_user/activate/<str:sign>/', user_activate, name = 'user_activate'),
	# path('profile/detail', profile, name = 'profile'),

	# Тут у нас все что связано с товарами
	path('order/add', add_order, name = 'add_order'), # странида добавления товара(только админ)
	path('order/delete/<int:pk>', order_delete, name = 'order_delete'), # страница удаления товара(только админ)
	path('order/change/<int:pk>', order_change, name = 'order_change'), # страница изменения товара (только админ)
	# path('order/detail', detail, name = 'detal'),

]