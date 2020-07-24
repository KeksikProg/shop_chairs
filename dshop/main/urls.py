from django.urls import path 
from .views import home
from .views import BbLogin, add_order,order_delete,order_change, other, ChangeUserInfo, UserPasswordChange, BbLogout
from .views import DeleteUserView 

app_name = 'main'

urlpatterns = [
	path('', home, name = 'home'),
	path('other/<str:page>/', other, name = 'other'),
	path('profile/login/', BbLogin.as_view(), name = 'login'),
	path('profile/change_info', ChangeUserInfo.as_view(), name = 'change_info'),
	path('profile/change_pass', UserPasswordChange.as_view(), name = 'change_pass'),
	path('profile/logout', BbLogout.as_view(), name = 'logout'),
	path('profile/delete_user', DeleteUserView.as_view(), name = 'delete_user'),
	path('order/add', add_order, name = 'add_order'),
	path('order/delete/<int:pk>', order_delete, name = 'order_delete'),
	path('order/change/<int:pk>', order_change, name = 'order_change'),

]