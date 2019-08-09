from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from account.models import OftyUser, OftyUserRentLord, DeliveryCase
import json


# Create your views here.
def login(request):
	# TODO: сделать тут POST запросы, когда будет интерфеечка
	if "user" not in request.POST:
		return HttpResponse("specify user, please", status=500)
	if "password" not in request.POST:
		return HttpResponse("specify password, please", status=500)

	user = authenticate(username=request.POST["user"], password=request.POST["password"])
	if user is not None:
		django_login(request, user)
		return HttpResponse("OK")
	else:
		return HttpResponse("login failed", status=500)


def logout(request):
	django_logout(request)
	if request.user.is_anonymous:
		return HttpResponse("OK")
	else:
		return HttpResponse("something going wrong with logout", status=500)


def login_page(request):
	return HttpResponse("Where is my login_page dude?")


def login_info(request):
	if not request.user.is_authenticated:
		return HttpResponse("You not loggined in. Go for /account/login with your user, password pair")
	else:
		return HttpResponse(f"You loggined as {request.user.username} ({request.user.id})")


def demo(request):
	params = {
		'user_name': request.user.username if not request.user.is_anonymous else "Anonymous",
		"user_id": request.user.id if not request.user.is_anonymous else "X"
	}
	return render(request, 'account/demo.html', params)


def password_set(request):
	if "password" not in request.POST:
		return HttpResponse("password not specified", status=500)
	if request.user.is_anonymous:
		return HttpResponse("you are not loggined yet", status=500)
	else:
		oldname = request.user.username
		request.user.set_password(request.POST["password"])
		request.user.save()
		user = authenticate(request, username=oldname, password=request.POST["password"])
		if user is not None:
			django_login(request, user)
		else:
			return HttpResponse("unpredictable password_set result", status=500)
		return HttpResponse("OK")


def delivery_get(request):
	if request.user.is_anonymous:
		return HttpResponse("you must be loggined in", status=500)
	cases = DeliveryCase.objects.filter(user=request.user)
	try:
		rent_lord = OftyUserRentLord.objects.get(user=request.user)
	except OftyUserRentLord.DoesNotExist:
		rent_lord = OftyUserRentLord.objects.create(user=request.user)
	ans = {
		"sklad": json.dumps(rent_lord.sklad),
		"metro": json.dumps(rent_lord.metro),
		"commentary": json.dumps(rent_lord.commentary),
		"cases": json.dumps([
			{
				"name": x.name,
				"value": x.value
			} for x in cases])
	}
	return JsonResponse(ans)


def delivery_set(request):
	if request.user.is_anonymous:
		return HttpResponse("you must be loggined in", status=500)

	if request.method != "POST":
		return HttpResponse("please use POST method for this page", status=500)

	must_be = ["cases", "sklad", "metro", "commentary"]
	for must in must_be:
		if must not in request.POST:
			return HttpResponse(f"There is no parameter {must}", status=500)
	try:
		delivery_cases = json.loads(request.POST["cases"])
		if type(delivery_cases) is not list:
			return HttpResponse("cases parameter must be a JSON list object", status=500)
	except json.JSONDecodeError:
		return HttpResponse("wrong data format (invalid JSON)", status=500)
	sklad = request.POST["sklad"]
	metro = request.POST["metro"]
	commentary = request.POST["commentary"]

	try:
		rent_lord = OftyUserRentLord.objects.get(user=request.user)
	except OftyUserRentLord.DoesNotExist:  # если записи нет - создаём её
		rent_lord = OftyUserRentLord.objects.create(user=request.user)

	rent_lord.sklad = sklad
	rent_lord.metro = metro
	rent_lord.commentary = commentary
	rent_lord.save()

	try:
		for case in delivery_cases:
			DeliveryCase.objects.create(user=request.user, name=case["name"], value=case["value"])
	except KeyError:
		return HttpResponse("invalid JSON string content", status=500)

	return HttpResponse("OK")


def time_set(request):
	return HttpResponse("time set not implemented")


def new_account(request):
	must = ["login", "password"]
	for m in must:
		if m not in request.POST:
			return HttpResponse(f"There is no parameter {m}", status=500)
	try:
		User.objects.get(username=request.POST['login'])
		return HttpResponse("login already exists", status=500)
	except User.DoesNotExist:
		new_user = User.objects.create_user(
			username=request.POST["login"],
			email="",
			password=request.POST['password'])
		OftyUser.objects.create(user=new_user)
		return HttpResponse("OK")
