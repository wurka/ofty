from django.urls import path
from . import views


urlpatterns = [
    path('get-my-orders', views.get_my_orders, {'mode': 'order'}, name='get-my-orders'),
    path('get-my-deals', views.get_my_orders, {'mode': 'deal'}, name='get-my-deals'),
    path('new-order', views.new_order, name='new-order'),
    path('reject-by-client', views.reject_by_client, name='reject-by-client'),
    path('reject-by-owner', views.reject_by_owner, name='reject-by-owner'),
    path('delete-by-client', views.delete_order, {'by_client': True}, name='delete-by-client'),
    path('delete-by-owner', views.delete_order, {'by_client': False}, name='delete-by-owner'),
]
