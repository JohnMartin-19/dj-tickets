import base64
from django.shortcuts import render
from .models import *
from django.http import JsonResponse,request
import json
import requests
import datetime
from django.views.decorators.csrf import csrf_exempt
from .utils import cookieCart,cartData,guestOrder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings



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

def callback(request):
    context = {}
    return render(request, 'store/callback.html')



####MPESA STK

# def get_access_token():
#     mpesa_auth_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

#     response = requests.get(
#         mpesa_auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret)
#     )
#     data = response.json()
#     print(data)
#     return data["access_token"]



def generate_access_token():
    consumer_key = "4NkzqcQNcpn7QA2TZ08z3wuT0tGDGQCE8t9hbsUSND7DBeWb"
    consumer_secret = "tiBILGN3tKsYc2VlG4LzXF96WMT4fSNuv3IBVu7QlgCbVaV2tst2g0mDjtF9zSCr"

    #choose one depending on you development environment
    #sandbox
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    #live
    #url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        
        encoded_credentials = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()

        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

        # Send the request and parse the response
        response = requests.get(url, headers=headers).json()
        print(response)
        # Check for errors and return the access token
        if "access_token" in response:
            return response["access_token"]
        else:
            raise Exception("Failed to get access token: " + response["error_description"])
    except Exception as e:
        raise Exception("Failed to get access token: " + str(e)) 



def stkpush(request):
    """
    STK push endpoint.
    """
    try:
        access_token = generate_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        print("headers-->", headers)
        business_short_code = '174379'
        pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        amount = data.get('amount')
        print(f"Phone number: {phone_number}, Amount: {amount}")
        web_name = "E-TICKETS"
        stk_password = base64.b64encode((business_short_code + pass_key + timestamp).encode('utf-8')).decode('utf-8')

        payload = {
            "BusinessShortCode": business_short_code,
            "Password": stk_password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://da8e-102-210-40-50.ngrok-free.app/callback/",
            "AccountReference": web_name,
            "TransactionDesc": "Payment of a ticket",
        }

        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            headers=headers,
            json=payload,
        )

        return JsonResponse(response.json())  # Corrected line

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Request error: {e}'}, status=500)
    except Exception as e:
        print(f"Error in stkpush: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@csrf_exempt  
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            callback_data = json.loads(request.body)
            # Process the callback data (update database, etc.)
            print("M-Pesa callback received:", callback_data)

            # Extract relevant information from the callback
            result_code = callback_data.get("Body", {}).get("stkCallback", {}).get("ResultCode")
            result_desc = callback_data.get("Body", {}).get("stkCallback", {}).get("ResultDesc")

            if result_code == 0:
                # Payment was successful
                print("Payment successful: ", result_desc)
                # Update database or session to mark payment as completed
                # Send success response to M-Pesa
                return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"}) 
            else:
                # Payment failed
                print(f"Payment failed: {result_desc}")
                return JsonResponse({"ResultCode": 1, "ResultDesc": "Payment failed"})

        except Exception as e:
            print(f"Error processing M-Pesa callback: {e}")
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Error"})
    else:
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid request method"})
