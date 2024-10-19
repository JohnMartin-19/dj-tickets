from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from .utils import cookieCart,cartData,guestOrder
# Create your views here.
def landing(request):
    context = {}
    return render(request, 'store/landing.html')



def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    events = Event.objects.all()
    context = {'events':events,'cartItems':cartItems }
    return render (request, 'store/store.html',context)



def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order,'cartItems':cartItems }
    return render (request, 'store/cart.html',context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

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

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        # Check if there is already an incomplete order
        order = Order.objects.filter(customer=customer, complete=False).first()
        
        # If no incomplete order exists, create a new one
        if not order:
            order = Order.objects.create(customer=customer, complete=False)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        # Update the order status to complete only if the total matches
        if abs(total - float(order.get_cart_total)) < 0.01:
            order.complete = True
        
        # Save the order (this will either create a new order or update the existing one)
        order.save()

        print(f"Total from frontend: {total}")
        print(f"Total from order: {float(order.get_cart_total)}")

        # Handle shipping if required
        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
    # Handle guest users here
        customer,order = guestOrder(request,data)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
             order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
