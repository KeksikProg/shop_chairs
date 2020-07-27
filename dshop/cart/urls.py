from django.urls import path
from .services import cart_add, cart_remove
from .views import cart_detail

urlpatterns = [
	path('detail/', cart_detail, name = 'cart_detail'),
	path('add/<int:product_id>/', cart_add, name = 'cart_add'),
	path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
]