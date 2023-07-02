from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name = "home"),
    path('product_list/', product_list, name = "product_list"),
    path('product_details/<int:id>', product_details, name = "product_details"),
    path('cart/', cart, name = "cart"),
    path('checkout/', checkout, name = "checkout"),
    path('account/', account, name = "account"),
    path('wishlist/', wishlist, name = "wishlist"),
    path('register/', registerUser, name = "register"),
    path('accounts/login/', loginUser, name = "login"),
    path('logout/', logoutUser, name = "logout"),
    path('contact/', contact, name = "contact"),
    path('profile/', profile, name = "profile"),
    path('address/', address, name = "address"),
    path('add_to_cart/', add_to_cart, name = "add_to_cart"),
    path('pluscart/', pluscart, name = "pluscart"),
    path('minuscart/', minuscart, name = "minuscart"),
    path('removecart/', removecart, name = "removecart"),
    path('paymentdone/', paymentdone, name = "paymentdone"),
    path('orders/', orders, name = "orders"),
    path('create-checkout-session/', create_checkout_session, name = "create-checkout-session"),
    path('payment-success/', paymentSuccess, name = "payment-success"),
    path('payment-cancel/', paymentCancel, name = "payment-cancel"),
]
