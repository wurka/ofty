from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	url(r'^login$', views.login),
	path('logout', views.logout),
	url(r'^login-page$', views.login_page),
	path('demo', views.demo),
	path('password-set', views.password_set),
	# path('delivery-set', views.delivery_set),
	# path('delivery-get', views.delivery_get),
	# path('time-set', views.time_set),
	# path('time-get', views.time_get),
	path('new-account', views.new_account, name='new-account'),
	path('alerts-set', views.alerts_set),
	path('alerts-get', views.alerts_get),
	path('about-me', views.about_me),
	path('get-settings', views.get_settings),
	path('save-avatar', views.save_avatar),
	path('save-info', views.save_info),
	path('save-work-time', views.save_work_time),
	path('save-notification', views.save_notification),
	path('save-blacklist', views.save_blacklist),
	path('save-rent', views.save_rent),
]
