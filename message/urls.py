from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
	url(r'^test/', views.test),
	path('demo', views.demo),
	path('my-conversations', views.my_conversations),
	path('new-conversation', views.new_conversation),

]
