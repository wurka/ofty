from django.urls import path
from . import views


urlpatterns = [
    path('get-my-orders', views.get_my_orders, name='get-my-orders'),
    path('new-order', views.new_order, name='new-order'),
    path('add-to-basket', views.add_to_basket, name='add-to-basket'),
]