from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null= True)
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class Event(models.Model): 
    title = models.CharField(default='title',max_length=20)
    digital = models.BooleanField(default = False, null=True, blank=True)
    description = models.CharField(default='describe',max_length= 200)
    date = models.DateField(null=True)
    ticket_price = models.FloatField(blank=True, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    location = models.CharField(max_length=50, null=True)
    max_ticket = models.IntegerField(default='0',null=True)
    image = models.ImageField(null=True,blank=True)
    
    def __str__(self):
        return self.title
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_booked = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True,blank=True)
    transaction_id = models.CharField(max_length=300, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        ticketItem = self.items.all()
        for item in ticketItem:
            if item.event.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderItems = self.items.all()
        total = sum([item.get_total for item in orderItems])
        return total
    
    def get_cart_items(self):
        orderItems = self.items.all()
        total = sum([item.quantity for item in orderItems ])
        return total
class TicketItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank= True, null=True, related_name='items')
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    

    @property
    def get_total(self):
        if not self.event:
            # Handle the case where the event is None
            print("No event linked to this TicketItem.")
            return 0  # or handle as you see fit

        # Ensure ticket_price is not None, default to 0 if it is
        ticket_price = self.event.ticket_price if self.event.ticket_price is not None else 0
        total = ticket_price * self.quantity
        #print(f"Calculating total: {ticket_price} * {self.quantity} = {total}")
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank= True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
 