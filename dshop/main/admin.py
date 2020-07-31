from django.contrib import admin
from .models import Bb, Client, Rubric, Comment, Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
	list_display = ('pk', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated')

	readonly_fields = ('created', 'updated')

	fields = (
		('first_name', 'last_name'),
		'email',
		('city', 'address', 'postal_code'),
		'paid',)

	# list_filter = ('paid', 'created', 'updated')

	inlines = (OrderItemInline,)




admin.site.register(Bb)
admin.site.register(Client)
admin.site.register(Rubric)
admin.site.register(Comment)
admin.site.register(Order, OrderAdmin)

# Register your models here.
