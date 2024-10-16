from django.shortcuts import render
from .models import *

# Create your views here.
def landing(request):
    context = {}
    return render(request, 'store/landing.html')

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.items.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'order':order}
    return render (request, 'store/cart.html',context)

def store(request):
    events = Event.objects.all()
    context = {'events':events}
    return render (request, 'store/store.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.items.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items':items, 'order':order}
    return render (request, 'store/checkout.html',context)