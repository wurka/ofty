from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	path('login', views.login, name='login'),
	path('logout', views.logout, name='logout'),
	path('demo', views.demo, name='demo'),
	path('password-set', views.password_set, name='password-set'),
	path('generate-verification-password', views.generate_verification_password, name='generate-verification-password'),
	path('check-verification-password', views.check_verification_password, name='check-verification-password'),
	# path('delivery-set', views.delivery_set),
	# path('delivery-get', views.delivery_get),
	# path('time-set', views.time_set),
	# path('time-get', views.time_get),
	path('new-account', views.new_account, name='new-account'),
	# path('alerts-set', views.alerts_set),
	# path('alerts-get', views.alerts_get),
	path('about-me', views.about_me, name='about-me'),
	path('get-settings', views.get_settings, name='get-settings'),
	path('save-avatar', views.save_avatar, name='save-avatar'),
	path('save-info', views.save_info, name='save-info'),
	path('save-work-time', views.save_work_time, name='save-work-time'),
	path('save-notification', views.save_notification, name='save-notification'),
	path('save-blacklist', views.save_blacklist, name='save-blacklist'),
	path('save-rent', views.save_rent, name='save-rent'),
]
