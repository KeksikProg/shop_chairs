from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path


class Client(AbstractUser):
	is_active = models.BooleanField(
		default = False,
		db_index = True,
		verbose_name = 'Активация')

	class Meta(AbstractUser.Meta):
		pass

class Rubric(models.Model):
	name = models.CharField(
		max_length = 30,
		db_index = True,
		unique = True,
		verbose_name = 'Название')
	
	order = models.SmallIntegerField(
		default = 0,
		db_index = True, 
		verbose_name = 'Порядок')

	def __str__(self):
		return self.name

class Bb(models.Model):
	rubric = models.ForeignKey(
		Rubric,
		on_delete = models.PROTECT,
		verbose_name = 'Рубрика')
	
	name = models.CharField(
		max_length = 50,
		verbose_name = 'Название')
	
	content = models.TextField(
		verbose_name = 'Описание')
	
	price = models.FloatField(
		default = 0,
		verbose_name = 'Цена')
	
	image = models.ImageField(
		blank = True,
		upload_to = get_timestamp_path,
		verbose_name = 'Изображение')
	
	def delete(self, *args, **kwargs):
		for ai in self.additionalimage_set.all():
			ai.delete()
		super().delete(*args, **kwargs)

	class Meta:
		verbose_name = 'Объявление'
		verbose_name_plural = 'Объявления'
		ordering = ['name']

class AdditionalImage(models.Model):
	bb = models.ForeignKey(Bb, 
		on_delete = models.CASCADE,
		verbose_name = 'Объявление')

	image = models.ImageField(
		upload_to = get_timestamp_path,
		verbose_name = 'Изображение')

	class Meta:
		verbose_name = 'Дополнительное Изображение'
		verbose_name_plural = 'Дополнительные изображения'

class Comment(models.Model):
	bb = models.ForeignKey(Bb,
		on_delete = models.CASCADE,
		verbose_name = 'Объявление')

	author = models.CharField(
		max_length = 40,
		verbose_name = 'Автор')

	content = models.TextField(
		verbose_name = 'Содержание')

	created_at = models.DateTimeField(
		auto_now_add = True,
		db_index = True,
		verbose_name = 'Добавлено')

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'


from django.dispatch import Signal
from .utilities import send_activation_notification
user_registrated = Signal(providing_args = ['instance']) # Тут мы из всех сигналов берем определенный по его ключу
def user_registrated_dispatcher(sender, **kwargs):
	send_activation_notification(kwargs['instance']) 
user_registrated.connect(user_registrated_dispatcher)
# Create your models here.
