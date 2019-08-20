from django.db import models
from account.models import OftyUser
from django.contrib.auth.models import User


# Create your models here.
class Conversation(models.Model):
	title = models.TextField(default="Conversation.title")


class ConversationMember(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)


class Message(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
	message = models.TextField(default="")
	image = models.TextField(default="")
	is_deleted = models.BooleanField(default=False)
