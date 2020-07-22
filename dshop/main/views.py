from django.shortcuts import render
from .models import Rubric, Bb
from django.contrib.auth.views import LoginView

def home(request):
	bbs = Bb.objects.all()[:10]
	context = {'bbs':bbs}
	return render(request, 'main/home.html', context)

class BbLogin(LoginView):
	template_name = 'main/login.html'

# Create your views here.
