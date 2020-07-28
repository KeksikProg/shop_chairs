from datetime import datetime
from os.path import splitext
from django.template.loader import render_to_string
from django.core.signing import Signer # Это для цифровой подписи
from dshop.settings import ALLOWED_HOSTS
from django.dispatch import Signal
from django.db.models.signals import post_save

def get_timestamp_path(instance, filename): # Тк эта функция не относится не к редакторам не к контроллерами не к моделям ,мы просто запишем её сюда
	return f'{datetime.now().timestamp()}{splitext(filename)[1]}'

signer = Signer()

def send_activation_notification(user):
	if ALLOWED_HOSTS:
		host = 'http://' + ALLOWED_HOSTS[0]
	else:
		host = 'http://localhost:8000'
	context = {'user':user, 'host':host, 'sign':signer.sign(user.username)}
	subj = render_to_string('email/activation_letter_subj.txt', context)
	body = render_to_string('email/activation_letter_body.txt', context)
	user.email_user(subj, body)


user_registrated = Signal(providing_args = ['instance']) # Тут мы из всех сигналов берем определенный по его ключу
def user_registrated_dispatcher(sender, **kwargs):
	send_activation_notification(kwargs['instance']) 
user_registrated.connect(user_registrated_dispatcher)

