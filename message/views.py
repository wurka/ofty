from django.http import HttpResponse
import re
import json
from django.contrib.auth.models import User
from .models import Conversation, ConversationMember

# Create your views here.


def test(request):
	return HttpResponse("OK")


def create_conversation(request):
	must_be = ["title", "members"]
	for must in must_be:
		if must not in request.POST:
			return HttpResponse(f"There is no parameter {must} in POST request", status=500)

	reg = re.compile("[a-zA-Zа-яА-Я0-9]")
	title = request.POST["title"]

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
