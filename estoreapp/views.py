from django.shortcuts import render, redirect
from .models import Product, Customer, Cart, OrderPlaced
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login , logout, authenticate
from django.contrib import messages
from .forms import MyProfileForm
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import stripe

stripe.api_key = 'XXXX'
# Create your views here.

def home(request):
	return render(request, 'index.html', {})

@login_required	
def product_list(request):
	product_list = Product.objects.filter(category = 'TW')
	return render(request, 'product-list.html', {'product_list':product_list})


@login_required	
def product_details(request, id):
	pro_list  = Product.objects.get(pk = id)
	already_in_cart = False
	already_in_cart = Cart.objects.filter(Q(product = pro_list.id) & Q(user = request.user)).exists()
	return render(request, 'product-detail.html', {'pro_list':pro_list, 'already_in_cart':already_in_cart})

@login_required	
def checkout(request):
	user = request.user
	add = Customer.objects.filter(user = user)
	cart_items = Cart.objects.filter(user = user)
	amount = 0.0
	shiping_cost = 1.0
	totalamount = 0.0
	cart_product = [price for price in Cart.objects.all() if price.user == request.user]
	if cart_product:
		for price in cart_product:
			tempamount = float((price.quantity * price.product.discount_price))
			amount += tempamount
		totalamount = amount+shiping_cost
	return render(request, 'checkout.html', {'add':add,
	'amount':amount,
	 'totalamount':totalamount,
	  'cart_items':cart_items})

@login_required	
def account(request):
	return render(request, 'my-account.html', {})
@login_required	
def wishlist(request):
	return render(request, 'wishlist.html', {})

def registerUser(request):
	frm = UserRegisterForm()
	if request.user.is_authenticated:
		return HttpResponseRedirect("/")
	else:
		frm = UserRegisterForm(request.POST)
		if frm.is_valid():
			messages.success(request, 'Congrates ! Register Successfully')
			frm.save()
			#return HttpResponseRedirect("register")

	return render(request, 'login.html', {"form":frm})

def loginUser(request):
	form = UserRegisterForm()
	if request.user.is_authenticated:
		return HttpResponseRedirect("/")
	else:
		if request.method =='POST':
			username = request.POST.get('username')
			password = request.POST.get('pwd')
			user=authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('product_list')
	return render(request, 'login.html', {'form':form})


def logoutUser(request):
	logout(request)
	return redirect("login")
@login_required	
def profile(request):
	if request.method == 'POST':
		form = MyProfileForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			zipcode = form.cleaned_data['zipcode']
			state = form.cleaned_data['state']
			user = Customer(
				user = request.user,
				name = name, 
				locality = locality, 
				city = city, 
				zipcode = zipcode, 
				state = state
			)
			user.save()
			messages.success(request, 'Your profile updated Successfully .')
	else:
		form = MyProfileForm()

	return render(request, 'profile.html', {'form':form})

@login_required	
def address(request):
	addrs = Customer.objects.filter(user = request.user)
	return render(request, 'my-account.html', {'addrs':addrs, 'active':'active'})


def contact(request):
	return render(request, 'contact.html', {})

@login_required
def add_to_cart(request):
	user = request.user
	product_id = request.GET.get('prod_id')
	product = Product.objects.get(id = product_id)
	Cart(user = user, product = product).save()
	return redirect('/cart')

@login_required	
def cart(request):
	carts = Cart.objects.filter(user = request.user)
	amount = 0.0
	shiping_cost = 1.0
	total_amount = 0.0
	cart_product = [price for price in Cart.objects.all() if price.user == request.user]
	if cart_product:
		for price in cart_product:
			tempamount = float((price.quantity * price.product.discount_price))
			amount += tempamount
		totalamount = amount + shiping_cost
		tamount = tempamount
		return render(request, 'cart.html', {'carts':carts, 
			'totalamount':totalamount, 
			'amount':amount, 'tamount':tamount})
	else:
		return render(request, 'emptycart.html', {})


def pluscart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
		c.quantity += 1
		c.save()
		amount = 0.0
		shiping_cost = 1.0
		cart_product = [price for price in Cart.objects.all() if price.user == request.user]
		if cart_product:
			for price in cart_product:
				tempamount = float((price.quantity * price.product.sell_price))
				amount += tempamount
			tamount = tempamount
			data = {
				'quantity':c.quantity,
				'amount':amount,
				'totalamount':amount + shiping_cost,
				}
			return JsonResponse(data)

def minuscart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
		c.quantity -= 1
		c.save()
		amount = 0.0
		shiping_cost = 1.0
		cart_product = [price for price in Cart.objects.all() if price.user == request.user]
		if cart_product:
			for price in cart_product:
				tempamount = float((price.quantity * price.product.sell_price))
				amount += tempamount
			tamount = tempamount
			data = {
				'quantity':c.quantity,
				'amount':amount,
				'totalamount':amount + shiping_cost,
				}
			return JsonResponse(data)


def removecart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
		c.quantity -= 1
		c.delete()
		amount = 0.0
		shiping_cost = 1.0
		cart_product = [price for price in Cart.objects.all() if price.user == request.user]
		if cart_product:
			for price in cart_product:
				tempamount = float((price.quantity * price.product.sell_price))
				amount += tempamount
		
			data = {
				'amount':amount,
				'totalamount':amount + shiping_cost
				}
			return JsonResponse(data)


def paymentdone(request):
	cust_id = request.GET.get('cust_id')
	customer = Customer.objects.get(id = cust_id)
	cart = Cart.objects.filter(user = request.user)
	for c in cart:
		OrderPlaced(user = request.user, customer = customer, 
			product = c.product, quantity = c.quantity ).save()
		c.delete()
	return redirect('orders')

@login_required	
def orders(request):
	od = OrderPlaced.objects.filter(user = request.user)
	return render(request, 'orders.html', {'od':od})


def create_checkout_session(request):
	if request.method == 'POST':
		checkout_session = stripe.checkout.Session.create(payment_method_types=['card'], line_items=[{'price_data': {'currency':'inr', 'unit_amount':1000, 'product_data':{'name':'Estore'}},'quantity': 1,},],mode='payment',success_url= 'http://127.0.0.1:8000/payment-success/',cancel_url='http://127.0.0.1:8000/payment-cancel',)
		return redirect(checkout_session.url, code=303)

def paymentSuccess(request):
	add = Customer.objects.filter(user = request.user)
	return render(request, 'checkout.html', {"payment_status":"success", 'add':add})

def paymentCancel(request):
	return render(request, 'confirmation.html', {"payment_status":"cancel"})













