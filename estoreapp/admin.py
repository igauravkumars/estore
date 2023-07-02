from django.contrib import admin
from .models import Customer, Product, Cart, OrderPlaced

# Register your models here.

#admin.site.register(Customer)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['id','name', 'sell_price', 'discount_price','description','brand', 'category', 'image']


@admin.register(Cart)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['id','user', 'product','quantity']

@admin.register(OrderPlaced)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['id','user','customer', 'product','quantity', 'order_date', 'status']
