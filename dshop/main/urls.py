from django.urls import path 
from .views import home
from .views import BbLogin, add_product,product_delete,product_change, other, ChangeUserInfo, UserPasswordChange, BbLogout
from .views import DeleteUserView, UserRegisterView, RegisterDoneView, user_activate
from .views import ClientPasswordResetView, ClientPasswordResetDone, ClientPasswordConfirmView
from .views import product_detail, comment_delete, order_create

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

	#Тут у нас будут урлы со сбросом пароля, потому что их доваольно много(да 3-4 штуки для ожной задачи многовато)
	path('profile/password_reset_form', ClientPasswordResetView.as_view(), name = 'password_reset_form'),
	path('profile/password_reset_done', ClientPasswordResetDone.as_view(), name = 'password_reset_done' ),
	path('profile/password_reset_confirm/<uidb64>/<token>', ClientPasswordConfirmView.as_view(), name = 'password_reset_confirm'),

	# Тут у нас все что связано с товарами
	path('product/add', add_product, name = 'add_product'), # странида добавления товара(только админ)
	path('product/delete/<int:pk>', product_delete, name = 'product_delete'), # страница удаления товара(только админ)
	path('product/change/<int:pk>', product_change, name = 'product_change'), # страница изменения товара (только админ)
	path('product/detail/<int:pk>', product_detail, name = 'detail'),
	path('product/detail/comment_delete/<int:comments>', comment_delete, name = 'comment_delete'),
	# path('product/detail', detail, name = 'detal'),

	# Заказы
	path('order/create', order_create, name = 'order_create'),

]