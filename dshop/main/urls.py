from django.urls import path 
from .views import home
from .views import BbLogin, add_order,order_delete,order_change

app_name = 'main'

urlpatterns = [
	path('', home, name = 'home'),
	path('profile/login/', BbLogin.as_view(), name = 'login'),
	path('order/add', add_order, name = 'add_order'),
	path('order/delete/<int:pk>', order_delete, name = 'order_delete'),
	path('order/change/<int:pk>', order_change, name = 'order_change'),
]