from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from account.models import OftyUser
import json


class ChatConsumer(WebsocketConsumer):
	def connect(self):
		print('connect')
		self.accept()
		try:
			async_to_sync(self.channel_layer.group_add)('groupName', self.channel_name)
		except ConnectionRefusedError:
			print('ZALEX, seems like redis not available in system')

	def disconnect(self, code):
		try:
			async_to_sync(self.channel_layer.group_discard('groupName', self.channel_name))
		except ConnectionRefusedError:
			print("ZALEX, seems like redis not available in system while disconnect function")

	def receive(self, text_data=None, bytes_data=None):
		print('received')
		async_to_sync(self.channel_layer.group_send)('groupName', {
			'type': 'chat.message',
			'message': text_data
		})

	def chat_message(self, event):
		print('chat message in buiseness')
		self.send(text_data=event["message"], type='xxxm')


class UserUpdateConsumer(WebsocketConsumer):
	@staticmethod
	def notifty_user(user: User):
		ofty_user = OftyUser.get_user(user)
		message = {
			'type': 'user.message',
			'content': {
				'new_messages': ofty_user.new_messages,
				'new_orders': ofty_user.new_orders,
				'new_deals': ofty_user.new_deals,
				'units_in_basket': ofty_user.units_in_basket,
				'other_updates': False,
			}
		}
		layer = get_channel_layer()
		try:
			async_to_sync(layer.group_send)(f'user_update_{user.id}', message)
		except ConnectionRefusedError:
			print('ZALEX, seems channel middleware (REDIS mb) offline.')

	def user_message(self, event):
		self.send(text_data=json.dumps(event["content"]))

	def connect(self):
		print('connecting to UserUpdateConsumer')
		print(self.scope['user'])
		me = self.scope['user']
		if me.is_anonymous:
			self.close()
		userid = int(self.scope['url_route']['kwargs']['userid'])
		if userid == me.id:
			self.accept()
			try:
				async_to_sync(self.channel_layer.group_add)(f'user_update_{me.id}', self.channel_name)
			except ConnectionRefusedError:
				print('ZALEX, seems like redis not available in system')

	def disconnect(self, code=1011):
		try:
			async_to_sync(self.channel_layer.group_discard('user_upda', self.channel_name))
		except ConnectionRefusedError:
			print("ZALEX, seems like redis not available in system while disconnect function")

	def receive(self, text_data=None, bytes_data=None):
		pass