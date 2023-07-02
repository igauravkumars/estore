from django.db import models
from django.contrib.auth.models import User


# Create your models here.

STATE_CHOICES = (
('Chandigarh','Chandigarh'),
('Punjab','Punjab'),
('Haryana', 'Haryana')
	)
class Customer(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField(max_length = 200)
	locality = models.CharField(max_length= 200)
	city = models.CharField(max_length = 50)
	zipcode = models.IntegerField()
	state = models.CharField(choices = STATE_CHOICES, max_length = 50)

	def __str__(self):
		return str(self.id)

CATEGORY_CHOICES = (
('M','Mobile'),
('L','Laptop'),
('TW','Top Wear'),
('BW','Bottom Wear'),
)
class Product(models.Model):
    name = models.CharField(max_length=254, default='')
    description = models.TextField()
    sell_price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2)
    brand = models.CharField(max_length = 100)
    category = models.CharField(choices = CATEGORY_CHOICES, max_length = 2)
    image = models.ImageField(upload_to='product_images')
    
    def __str__(self):
        return str(self.id)


class Cart(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	quantity = models.PositiveIntegerField(default = 1)

	def __str__(self):
		return str(self.id)

	@property
	def total_cost(self):
		return self.quantity*self.product.discount_price

PRODUCT_STATUS = (
('Accepted', 'Accepted'),
('Packed', 'Packed'),
('On the way', 'On the way'),
('Delivered', 'Delivered'),
('Cancel', 'Cancel'),
)

class OrderPlaced(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	quantity = models.PositiveIntegerField(default = 1)
	order_date = models.DateTimeField(auto_now_add = True)
	status = models.CharField(choices = PRODUCT_STATUS ,max_length = 50, default = 'pending')

	@property
	def total_cost(self):
		return self.quantity*self.product.discount_price
