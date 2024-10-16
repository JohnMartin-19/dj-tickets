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
    price = models.FloatField()
    digital = models.BooleanField(default = False, null=True, blank=True)
    description = models.CharField(default='describe',max_length= 200)
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    location = models.CharField(max_length=50, null=True)
    max_ticket = models.IntegerField(default='0',null=True)
    #image
    
    def __str__(self):
        return self.title
    
class Ticket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_booked = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True,blank=True)
    transaction_id = models.CharField(max_length=300, null=True)

    def __str__(self):
        return str(self.id)
    
class TicketItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, blank= True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank= True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address