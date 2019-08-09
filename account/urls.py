from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	url(r'^login$', views.login),
	path('logout', views.logout),
	url(r'^login-page$', views.login_page),
	url(r'^status$', views.login_info),
	path('demo', views.demo),
	path('password-set', views.password_set),
	path('delivery-set', views.delivery_set),
	path('delivery-get', views.delivery_get),
	path('time-set', views.time_set),
	path('new-account', views.new_account)
]
