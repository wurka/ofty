from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from account.models import OftyUser, OftyUserRentLord, DeliveryCase
import json
from PIL import Image
from io import BytesIO
import os
from datetime import datetime


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
		"user_id": request.user.id if not request.user.is_anonymous else "X",
		"time": (datetime.now()-datetime(1970, 1, 1)).total_seconds()
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
	if request.user.is_anonymous:
		return HttpResponse("you must be loggined in", status=401)

	for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
		for attribute in ["[time-from]", "[time-to]", "[enable]"]:
			if day+attribute not in request.POST:
				return HttpResponse(f"there is no parameter {day}", status=500)

	for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
		for attribute in ["[time-from]", "[time-to]"]:
			value = request.POST[(day + attribute)]
			splitted = value.split(":")
			if len(splitted) != 2:
				return HttpResponse(f"time must be on format hh:mm, not {value}", status=500)
			try:
				h = int(splitted[0])
				m = int(splitted[1])
				if h < 0 or h > 23:
					return HttpResponse(f"hours must be from 0 to 23, not {splitted[0]}")
				if m < 0 or m > 59:
					return HttpResponse(f"minutes must be from 0 to 59, not {splitted[1]}")

			except ValueError:
				HttpResponse(f"hour and minute must be valid integers. invalid value: {value}", status=500)

	try:
		lord = OftyUserRentLord.objects.get(user=request.user)
	except OftyUserRentLord.DoesNotExist:
		lord = OftyUserRentLord.objects.create(user=request.user)

	try:
		lord.mon_enable = bool(json.loads(request.POST["mon[enable]"]))
		lord.mon_start_h = int(request.POST["mon[time-from]"].split(":")[0])
		lord.mon_start_m = int(request.POST["mon[time-from]"].split(":")[1])
		lord.mon_stop_h = int(request.POST["mon[time-to]"].split(":")[0])
		lord.mon_stop_m = int(request.POST["mon[time-to]"].split(":")[1])

		lord.tue_enable = bool(json.loads(request.POST["tue[enable]"]))
		lord.tue_start_h = int(request.POST["tue[time-from]"].split(":")[0])
		lord.tue_start_m = int(request.POST["tue[time-from]"].split(":")[1])
		lord.tue_stop_h = int(request.POST["tue[time-to]"].split(":")[0])
		lord.tue_stop_m = int(request.POST["tue[time-to]"].split(":")[1])

		lord.wed_enable = bool(json.loads(request.POST["wed[enable]"]))
		lord.wed_start_h = int(request.POST["wed[time-from]"].split(":")[0])
		lord.wed_start_m = int(request.POST["wed[time-from]"].split(":")[1])
		lord.wed_stop_h = int(request.POST["wed[time-to]"].split(":")[0])
		lord.wed_stop_m = int(request.POST["wed[time-to]"].split(":")[1])

		lord.thu_enable = bool(json.loads(request.POST["thu[enable]"]))
		lord.thu_start_h = int(request.POST["thu[time-from]"].split(":")[0])
		lord.thu_start_m = int(request.POST["thu[time-from]"].split(":")[1])
		lord.thu_stop_h = int(request.POST["thu[time-to]"].split(":")[0])
		lord.thu_stop_m = int(request.POST["thu[time-to]"].split(":")[1])

		lord.fri_enable = bool(json.loads(request.POST["fri[enable]"]))
		lord.fri_start_h = int(request.POST["fri[time-from]"].split(":")[0])
		lord.fri_start_m = int(request.POST["fri[time-from]"].split(":")[1])
		lord.fri_stop_h = int(request.POST["fri[time-to]"].split(":")[0])
		lord.fri_stop_m = int(request.POST["fri[time-to]"].split(":")[1])

		lord.sat_enable = bool(json.loads(request.POST["sat[enable]"]))
		lord.sat_start_h = int(request.POST["sat[time-from]"].split(":")[0])
		lord.sat_start_m = int(request.POST["sat[time-from]"].split(":")[1])
		lord.sat_stop_h = int(request.POST["sat[time-to]"].split(":")[0])
		lord.sat_stop_m = int(request.POST["sat[time-to]"].split(":")[1])

		lord.sun_enable = bool(json.loads(request.POST["sun[enable]"]))
		lord.sun_start_h = int(request.POST["sun[time-from]"].split(":")[0])
		lord.sun_start_m = int(request.POST["sun[time-from]"].split(":")[1])
		lord.sun_stop_h = int(request.POST["sun[time-to]"].split(":")[0])
		lord.sun_stop_m = int(request.POST["sun[time-to]"].split(":")[1])
		lord.save()
	except ValueError:
		return HttpResponse("invalid syntax", status=500)
	except IndexError:
		return HttpResponse("time must be in format hh:mm", status=500)

	return HttpResponse("OK")


def time_get(request):
	if request.user.is_anonymous:
		return HttpResponse("you must be loggined in", status=401)

	try:
		lord = OftyUserRentLord.objects.get(user=request.user)
	except OftyUserRentLord.DoesNotExist:
		lord = OftyUserRentLord.objects.create(user=request.user)

	ans = {
		"mon": {
			"time-from": f'{lord.mon_start_h:02d}:{lord.mon_start_m:02d}',
			"time-to": f'{lord.mon_stop_h:02d}:{lord.mon_stop_m:02d}',
			"enable": str(lord.mon_enable)
		},
		"tue": {
			"time-from": f'{lord.tue_start_h:02d}:{lord.tue_start_m:02d}',
			"time-to": f'{lord.tue_stop_h:02d}:{lord.tue_stop_m:02d}',
			"enable": str(lord.tue_enable)
		},
		"wed": {
			"time-from": f'{lord.wed_start_h:02d}:{lord.wed_start_m:02d}',
			"time-to": f'{lord.wed_stop_h:02d}:{lord.wed_stop_m:02d}',
			"enable": str(lord.wed_enable)
		},
		"thu": {
			"time-from": f'{lord.thu_start_h:02d}:{lord.thu_start_m:02d}',
			"time-to": f'{lord.thu_stop_h:02d}:{lord.thu_stop_m:02d}',
			"enable": str(lord.thu_enable)
		},
		"fri": {
			"time-from": f'{lord.fri_start_h:02d}:{lord.fri_start_m:02d}',
			"time-to": f'{lord.fri_stop_h:02d}:{lord.fri_stop_m:02d}',
			"enable": str(lord.fri_enable)
		},
		"sat": {
			"time-from": f'{lord.sat_start_h:02d}:{lord.sat_start_m:02d}',
			"time-to": f'{lord.sat_stop_h:02d}:{lord.sat_stop_m:02d}',
			"enable": str(lord.sat_enable)
		},
		"sun": {
			"time-from": f'{lord.sun_start_h:02d}:{lord.sun_start_m:02d}',
			"time-to": f'{lord.sun_stop_h:02d}:{lord.sun_stop_m:02d}',
			"enable": str(lord.sun_enable)
		}
	}

	return JsonResponse(ans)


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


def save_avatar(request):
	if request.user.is_anonymous:
		return HttpResponse("you must be loggined in", status=500)

	avatar_file_folder = os.path.join("user_uploads", f"user_{request.user.id}")

	os.makedirs(avatar_file_folder, exist_ok=True)

	if "avatar" not in request.FILES:
		return HttpResponse("there is no <avatar> in FILES", status=500)
	chunks = request.FILES["avatar"].chunks()

	file = BytesIO()
	for chunk in chunks:
		file.write(chunk)

	img = Image.open(file)
	width, height = img.size
	min_size = min(width, height)
	left = width/2.0 - min_size/2.0
	top = height/2.0 - min_size/2.0
	right = width/2.0 + min_size/2.0
	bottom = height/2.0 + min_size/2.0
	img = img.crop((left, top, right, bottom))
	img_170 = img.resize((170, 170), Image.BICUBIC)
	img_71 = img.resize((71, 71), Image.BICUBIC)
	avatar_file_path = os.path.join(avatar_file_folder, "avatar-170.png")
	img_170.save(avatar_file_path, "PNG")
	avatar_file_path = os.path.join(avatar_file_folder, "avatar-71.png")
	img_71.save(avatar_file_path, "PNG")

	return HttpResponse("OK")
