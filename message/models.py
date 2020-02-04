from django.db import models
from account.models import OftyUser
from django.contrib.auth.models import User
from datetime import datetime
import pytz

# Create your models here.
class Conversation(models.Model):
	title = models.TextField(default="Conversation.title")
	icon = models.TextField(default="")  # имя файла

	@staticmethod
	def get_icon_url(file_name):
		return f"/static/conversationimages/{file_name}"


class ConversationMember(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
	muted = models.BooleanField(default=False)  # заглушить информирование о новых сообщениях в этой беседе
	is_important = models.BooleanField(default=False)  # диалог помечен как важный для этого пользователя
	abandoned = models.BooleanField(default=False)  # из этого диалога пользователь ушёл


class Message(models.Model):
	# owner of msg
	owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="message_owner")
	# write this message
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="message_author")
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
	message = models.TextField(default="")
	image = models.TextField(default="")
	is_deleted = models.BooleanField(default=False)
	sent = models.BooleanField(default=True)  # сообщение отправлено (чтобы это не значило)
	creation_time = models.DateTimeField(default=datetime(1970, 1, 1, tzinfo=pytz.UTC))
	# поле типа сообщения (может быть message или date).date - плашка дня
	message_type = models.TextField(default="message")
	read = models.BooleanField(default=False)  # сообщение было прочитано получателем
