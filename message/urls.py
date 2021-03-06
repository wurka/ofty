from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
	url(r'^test/', views.test),
	path('demo', views.demo),
	path('demo-gui', views.demo_gui),
	path('my-conversations', views.my_conversations),
	path('new-conversation', views.new_conversation),
	path('conversation-view', views.conversation_view),
	path('get-before', views.get_before),
	path('get-after', views.get_after),
	path('new-message', views.new_message),
]
