from django.urls import path
from . import views

urlpatterns = [
    path('',views.landing,name ='landing'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart,name='cart'),
    path('checkout/', views.checkout, name ='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name="process_order"),
    path('stk_push/',views.stkpush, name = 'stk push'),
    path('mpesa_callback/',views.callback, name = 'call_back_url')
]