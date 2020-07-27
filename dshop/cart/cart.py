from decimal import Decimal
from django.conf import settings
from main.models import Bb

class Cart():

	def __init__(self, request):
		'''Инициализируем корзину прямо тут'''
		self.session = request.session # Тут мы говорим то что self сессия равна сессии пользователя 
		cart = self.session.get(settings.CART_SESSION_ID) # Тут мы пытаемся извечь из сессии пользователя ключ в котором определяется корзина
		if not cart:
			# Если вдруг так получилось что корзины не оказалось 
			cart = self.session[settings.CART_SESSION_ID] = {} # то мы просто создаем новую коризну (пока что пустую потому что человек туда ничего не добавил)
		self.cart = cart # и поле карт либо равно тому что человек уже добавлял в корзину либо она пустая 

	def __iter__(self):
		'''Перебор элементов в корзине и получение прдуктов из базы данных'''
		
		product_ids = self.cart.keys()
		# Получение списка ключей всех товаров в корзине
		products = Bb.objects.filter(id__in=product_ids)
		# делаем список из всех товаров, беря их из базы данных по их ключам
		for product in products: 
			self.cart[str(product.pk)]['product'] = product
			'''Тут как я понял мы просто переделываем из ключей товаров в полноценные записи и лобавдяя их в сессию'''

		'''Тут ниже мы цену преобразуем обратно в деситичное число и добавляем атрибуt total_price который высвечивает полную цену учитывая кол-во товаров в корзине'''
		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['qua']
			yield item

	def __len__(self):
		'''Тут мы будем выводить подчет всех товаров к=в корзине'''
		return sum(item['qua'] for item in self.cart.values())

	def add_or_update(self, product, qua=1, update_qua = False):
		'''Добавить продукт в корзину или обновить его кол-во'''

		product_id = str(product.pk) # Тут мы берем пк товара и преобразовывем в стр чтобы было удобнее работать
		if product_id not in self.cart: # если такого товара в корзине ещё нет то
			self.cart[product_id] = {'qua':0, # под ключом пк товара делаем его кол-во и цену (тоже в стр чтобы было удобнее работать)
									 'price':str(product.price)}

		if update_qua: # если же мы хотим обновить кол-во товаров то мы добавляем это число на место прошлого 
			self.cart[product_id]['qua'] = qua
		else: # а если не хотим то по умолчанию ставим 1 
			self.cart[product_id]['qua'] += qua

		self.save() # и все это сохраняем 

	def save(self):
		'''для сохранения изменений в сессии'''
		
		# тут мы обновляем сессию 
		self.session[settings.CART_SESSION_ID] = self.cart
		# и ещё нужно отметить сессию как измененую 
		self.session.modified = True

	def remove(self, product):
		'''Удаление товара из корзины'''

		product_id = str(product.pk)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def get_total_price(self):
		'''Подсчет стоимости всех товаров в коризну '''
		return sum(Decimal(item['price']) * item['qua'] for item in self.cart.values())

	def clear(self):
		'''Удаление корзины'''

		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True

