from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path



class Client(AbstractUser):
	'''Модель для пользователей (тут добавили только поле is_active чтобы сделать регистрацию с активацией'''
	is_active = models.BooleanField(
		default = False,
		db_index = True,
		verbose_name = 'Активация')

	class Meta(AbstractUser.Meta):
		pass

class Rubric(models.Model):
	'''Модель для рубрик'''
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
	'''Модель для просто товаров'''
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
	'''Модель для дополнительных изображений(товары)'''
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
	'''модель для комментариев'''
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

class Order(models.Model):
	'''ТУт модель для создания заказов'''
	first_name = models.CharField( # Имя
		max_length=50)
	last_name = models.CharField( # фамилия
    	max_length=50)
	email = models.EmailField() #  электронная почта
	address = models.CharField( # адрес
    	max_length=250)
	postal_code = models.CharField( # код региона
    	max_length=20)
	city = models.CharField( # город
    	max_length=100)
	created = models.DateTimeField( #  когда заказ создан
    	auto_now_add=True)
	updated = models.DateTimeField( # когда заказ обновлялся
    	auto_now=True)
	paid = models.BooleanField( # был ли заказ уже оплачен
    	default=False)

	class Meta:
		ordering = ['-created']
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'


	def __str__(self):
		return f'Order {self.pk}'

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
	order = models.ForeignKey(Order,
		related_name = 'items',
		on_delete = models.CASCADE)
	product = models.ForeignKey(Bb,
		related_name = 'order_item',
		on_delete = models.CASCADE)
	price = models.FloatField(
		default = 0,
		verbose_name = 'Цена')
	qua = models.PositiveIntegerField(default = 1)


	def __str__(self):
		return f'{self.pk}'

	def get_cost(self):
		return self.price * self.qua





from django.dispatch import Signal
from .utilities import send_activation_notification
user_registrated = Signal(providing_args = ['instance']) # Тут мы из всех сигналов берем определенный по его ключу
def user_registrated_dispatcher(sender, **kwargs):
	send_activation_notification(kwargs['instance']) 
user_registrated.connect(user_registrated_dispatcher)
# Create your models here.
