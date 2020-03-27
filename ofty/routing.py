from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import ofty.consumers
from django.urls import path


application = ProtocolTypeRouter({
	# Empty for now (http->django views is added by default)
	'websocket': AuthMiddlewareStack(
		URLRouter([
			path('ws/connect', ofty.consumers.ChatConsumer),
			path('ws/user_update/<int:userid>', ofty.consumers.UserUpdateConsumer),
		])
	)
})
