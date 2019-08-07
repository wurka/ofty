from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
	url(r'^test/', views.test),
	path('demo', views.demo),
	path('get-my-conversations', views.get_my_conversations),

]
