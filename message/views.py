from django.http import HttpResponse
from django.shortcuts import render
import re
import json
from django.contrib.auth.models import User
from .models import Conversation, ConversationMember, Message
from django.http import JsonResponse
from datetime import datetime

# Create your views here.
def logged(method):
	def inner(request):
		if request.user.is_anonymous:
			return HttpResponse("you must be loggined in", status=401)
		return method(request)
	return inner


def post_with_parameters(*args):
	def decor(method):
		def response(request):
			if request.method != "POST":
				return HttpResponse(f"please use POST request, not {request.method}", status=500)
			for param in args:
				if param not in request.POST:
					return HttpResponse(f"there is no parameter {param}", status=500)
			return method(request)
		return response
	return decor


def get_with_parameters(*args):
	def decor(method):
		def response(request):
			if request.method != "GET":
				return HttpResponse(f"please use GET request, not {request.method}", status=500)
			for param in args:
				if param not in request.GET:
					return HttpResponse(f"there is no parameter {param}", status=500)
			return method(request)
		return response
	return decor


def test(request):
	return HttpResponse("OK")


def demo(request):
	params = {
		"username": request.user.username if not request.user.is_anonymous else "Anonymous",
		"userid": request.user.id if not request.user.is_anonymous else "X",
	}
	return render(request, 'message/demo.html', params)


def demo_gui(request):
	return render(request, 'message/demo-gui.html')


def new_conversation(request):
	must_be = ["name", "members"]
	for must in must_be:
		if must not in request.POST:
			return HttpResponse(f"There is no parameter {must} in POST request", status=500)

	reg = re.compile("[a-zA-Zа-яА-Я0-9\s]+")
	title = request.POST["name"]

	checked = False
	match = reg.match(title)
	if match:
		verifyed_title = match.group()
		if verifyed_title == title:
			checked = True

	if not checked:
		text = "Invalid title: title must contains only numbers, letters and spaces"
		return HttpResponse(text, status=500)

	# проверка всех указанных пользователей на наличие на сайте
	try:
		members_id = json.loads(request.POST["members"])
		if not type(members_id) is list:
			return HttpResponse("Wrong parameter <members>. POST[members] must be list", status=500)

		wrongid = 0
		try:
			for mid in members_id:
				wrongid = int(mid)
				User.objects.get(id=wrongid)
		except ValueError:
			return HttpResponse("Wrong parameter value: all members must be spec as int ids", status=500)
		except User.DoesNotExist:
			return HttpResponse(f"There is no user with id {wrongid}", status=500)

	except KeyError:
		return HttpResponse("Uknown error in create_conversation", status=500)
	except json.JSONDecodeError:
		return HttpResponse("invalid value: members must be valid JSON array", status=500)

	# все пользователи валидны, а title проверен
	new_conversation = Conversation(
		title=title
	)
	new_conversation.save()

	new_members = [ConversationMember(
		user=User.objects.get(id=int(mid)),
		conversation=new_conversation
	) for mid in members_id]
	ConversationMember.objects.bulk_create(new_members)
	return HttpResponse("OK")


def add_member_to_conversation(request):
	return HttpResponse("OK")


def my_conversations(request):
	# взять Юзера
	me = ConversationMember.objects.filter(user=request.user)
	ans = list()
	for m in me:
		members = ConversationMember.objects.filter(conversation=m.conversation, abandoned=False)

		ans.append({
			"id": m.conversation.id,
			"title": m.conversation.title,
			"photo": Conversation.get_icon_url(m.conversation.icon),
			"users": [
				{
					"id": member.user.id,
					"name": member.user.username,
					"photo": f"/static/user_{member.user.id}/avatar-71.png"
				} for member in members],
			"mute": m.muted,
			"flag": m.is_important,
			"active": not m.abandoned,
		})
	return JsonResponse(ans, safe=False)


@logged
@get_with_parameters("conversation", "beforeid", "size")
def get_before(request):
	"""получить сообщения из беседы [id]. все они будут предшествовать сообщению с id==[offset].
	количество сообщений - size
	ПРИМЕЧАНИЕ: если offset == -1 => вернутся последние сообщения из диалога
	"""

	try:
		convers = Conversation.objects.get(id=int(request.GET['conversation']))
		ConversationMember.objects.get(conversation=convers, user=request.user)
		offset = int(request.GET["beforeid"])
		size = int(request.GET["size"])

		if offset == -1:
			msgs = Message.objects.filter(
				conversation=convers, owner=request.user, is_deleted=False).order_by("id")
		else:
			msgs = Message.objects.filter(
				id__lt=offset,
				conversation=convers, owner=request.user, is_deleted=False).order_by("id")

		length = len(msgs)
		start = max(length - size, 0)
		stop = length
		msgs = msgs[start: stop]
	# такой беседы нет или пользователь не является её участником
	except (ConversationMember.DoesNotExist, Conversation.DoesNotExist):
		return HttpResponse(f"there is no conversation with id {request.GET['conversation']}", status=404)
	except ValueError:
		return HttpResponse("conversation, size and beforeid must be valid integers", status=500)
	except Exception as e:
		print(e)
		return HttpResponse(f"Unexpected error: {str(e)}", status=500)

	ans = [{
		"id": m.id,
		"text": m.message,
		"image": m.image,
		"with-image": False if m.image == "" else True,
		"author": m.author.id,
		"author_name": m.author.username,
		"mine": m.author.id == m.owner.id,
		"sent": m.sended,
		"datetime": {
			"year": m.creation_time.year,
			"month": m.creation_time.month,
			"day": m.creation_time.day,
			"hour": m.creation_time.hour,
			"minute": m.creation_time.minute,
			"second": m.creation_time.second
		},
		"type": m.message_type,  # message/date
		"read": m.read,
	} for m in msgs]

	return JsonResponse(ans, safe=False)


@logged
@get_with_parameters("conversation", "afterid", "size")
def get_after(request):
	"""
	Запрос сообщений из беседы [conversation], после сообщения [afterid]. Максимальное количество - size
	:return: json массив
	"""
	try:
		convers = Conversation.objects.get(id=int(request.GET['conversation']))
		ConversationMember.objects.get(conversation=convers, user=request.user)
		afterid = int(request.GET["afterid"])
		size = int(request.GET["size"])

		msgs = Message.objects.filter(
			id__gt=afterid,
			conversation=convers, owner=request.user, is_deleted=False).order_by("id")

		length = len(msgs)
		msgs = msgs[0:min(size, length)]
	# такой беседы нет или пользователь не является её участником
	except (ConversationMember.DoesNotExist, Conversation.DoesNotExist):
		return HttpResponse(f"there is no conversation with id {request.GET['conversation']}", status=404)
	except ValueError:
		return HttpResponse("conversation, size and afterid must be valid integers", status=500)
	except Exception as e:
		print(e)
		return HttpResponse(f"Unexpected error: {str(e)}", status=500)

	ans = [{
		"id": m.id,
		"text": m.message,
		"image": m.image,
		"with-image": False if m.image == "" else True,
		"author": m.author.id,
		"author_name": m.author.username,
		"mine": m.author.id == m.owner.id,
		"sent": m.sent,
		"datetime": {
			"year": m.creation_time.year,
			"month": m.creation_time.month,
			"day": m.creation_time.day,
			"hour": m.creation_time.hour,
			"minute": m.creation_time.minute,
			"second": m.creation_time.second
		},
		"type": m.message_type,
		"read": m.read,
	} for m in msgs]

	return JsonResponse(ans, safe=False)


@logged
@get_with_parameters("id", "offset", "size")
def conversation_view(request):
	"""
	просмотр беседы с id. От конца беседы смещение на offset. Всего выдается максимум size сообщений
	:param request:
	:return:
	"""
	try:
		convers = Conversation.objects.get(id=int(request.GET['id']))
		ConversationMember.objects.get(conversation=convers, user=request.user)
		offset = int(request.GET["offset"])
		size = int(request.GET["size"])

		if offset == -1:
			msgs = Message.objects.filter(
				conversation=convers, owner=request.user, is_deleted=False).order_by("id")
		else:
			msgs = Message.objects.filter(
				id__lt=offset,
				conversation=convers, owner=request.user, is_deleted=False).order_by("id")

		length = len(msgs)
		start = max(length-size, 0)
		stop = length
		msgs = msgs[start : stop]
	# такой беседы нет или пользователь не является её участником
	except (ConversationMember.DoesNotExist, Conversation.DoesNotExist):
		return HttpResponse(f"there is no conversation with id {request.GET['id']}", status=404)
	except ValueError:
		return HttpResponse("conversation, size and offset must be valid integers", status=500)
	except Exception as e:
		print(e)

	ans = [{
		"id": m.id,
		"text": m.message,
		"image": m.image,
		"with-image": False if m.image == "" else True,
		"author": m.author.id,
		"author_name": m.author.username,
		"mine": False  # m.author.id == m.owner.id
	} for m in msgs]

	return JsonResponse(ans, safe=False)


@logged
@post_with_parameters("conversation", "message")
def new_message(request):
	try:
		convers = Conversation.objects.get(id=request.POST["conversation"])
		ConversationMember.objects.get(conversation=convers, user=request.user)
	except (Conversation.DoesNotExist, ConversationMember.DoesNotExist):
		return HttpResponse(f"there is no conversation with id {request.POST['conversation']}", status=404)
	except ValueError:
		value = request.POST['conversation']
		return HttpResponse(f"conversation must be valid integer, not {value}", status=500)

	# все учавствующие в беседе
	members = ConversationMember.objects.filter(conversation=convers, abandoned=False)
	msgs = [Message(
		owner=m.user,
		author=request.user,
		message=request.POST["message"],
		conversation=convers,
		creation_time=datetime.now()) for m in members]
	Message.objects.bulk_create(msgs)

	return HttpResponse("OK")

