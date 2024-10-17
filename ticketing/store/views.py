from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

# Create your views here.
def landing(request):
    context = {}
    return render(request, 'store/landing.html')



def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.items.all()
        cartItems = order.get_cart_items()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems = ['get_cart_items']
        
    events = Event.objects.all()
    context = {'events':events,'cartItems':cartItems }
    return render (request, 'store/store.html',context)



def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.items.all()
        cartItems = order.get_cart_items()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems = ['get_cart_items']

    context = {'items':items, 'order':order,'cartItems':cartItems }
    return render (request, 'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.items.all()
        cartItems = order.get_cart_items()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems = ['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render (request, 'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    eventId = data['eventId']
    action = data['action']

    print('eventId:', eventId)
    print('action:',action)

    customer = request.user.customer
    event = Event.objects.get(id=eventId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    ticketItem, created = TicketItem.objects.get_or_create(order=order, event=event)

    if action == 'add':
        ticketItem.quantity = (ticketItem.quantity + 1)
    elif action == 'remove':
        ticketItem.quantity = (ticketItem.quantity - 1)
    
    ticketItem.save()

    if ticketItem.quantity <= 0:
        ticketItem.delete()

    return JsonResponse('Item was added', safe=False)