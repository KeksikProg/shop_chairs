from django.urls import path 
from .views import home
from .views import BbLogin

app_name = 'main'

urlpatterns = [
	path('', home, name = 'home'),
	path('profile/login/', BbLogin.as_view(), name = 'login'),
]