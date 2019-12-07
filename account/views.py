from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from account.models import OftyUser, OftyUserWorkTime, DeliveryCase, BlackListInstance
from units.models import Unit
import json
from PIL import Image
from io import BytesIO
import os
from datetime import datetime


# Create your views here.
def logged_and_post(method):
	def inner(request):
		if request.user.is_anonymous:
			return HttpResponse("you must be loggined in", status=401)
		if request.method != "POST":
			return HttpResponse("please use POST method", status=500)
		return method(request)
	return inner


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


def login(request):
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


@logged_and_post
def logout(request):
	django_logout(request)
	if request.user.is_anonymous:
		return HttpResponse("OK")
	else:
		return HttpResponse("something going wrong with logout", status=500)


def login_page(request):
	return HttpResponse("Where is my login_page dude?")


def demo(request):
	params = {
		'user_name': request.user.username if not request.user.is_anonymous else "Anonymous",
		"user_id": request.user.id if not request.user.is_anonymous else "X",
		"time": (datetime.now()-datetime(1970, 1, 1)).total_seconds()
	}
	return render(request, 'account/demo.html', params)


@logged_and_post
def password_set(request):
	if "password" not in request.POST:
		return HttpResponse("password not specified", status=500)
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


@logged_and_post
def save_avatar(request):
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


@logged_and_post
def alerts_set(request):
	for param in [
		"enable_push", "enable_sound_alert", "enable_sms_new_order", "enable_sms_startstop",
		"enable_email_new_order", "enable_email_startstop"]:
		if param not in request.POST:
			return HttpResponse(f"there is no parameter {param}", status=500)

	try:
		ofty_user = OftyUser.objects.get(user=request.user)
	except OftyUser.DoesNotExist:
		ofty_user = OftyUser.objects.create(user=request.user)

	try:
		ofty_user.enable_push = json.loads(request.POST["enable_push"])
		ofty_user.enable_sound_alert = json.loads(request.POST["enable_sound_alert"])
		ofty_user.enable_sms_new_order = json.loads(request.POST["enable_sms_new_order"])
		ofty_user.enable_sms_startstop = json.loads(request.POST["enable_sms_startstop"])
		ofty_user.enable_email_new_order = json.loads(request.POST["enable_email_new_order"])
		ofty_user.enable_email_startstop = json.loads(request.POST["enable_email_startstop"])
		ofty_user.save()
	except ValueError:
		return HttpResponse("invalid syntax", status=500)

	return HttpResponse("OK")


@logged
def alerts_get(request):
	try:
		ofty_user = OftyUser.objects.get(user=request.user)
	except OftyUser.DoesNotExist:
		ofty_user = OftyUser.objects.create(user=request.user)

	ans = {
		"enable_push": ofty_user.enable_push,
		"enable_sound_alert": ofty_user.enable_sound_alert,
		"enable_sms_new_order": ofty_user.enable_sms_new_order,
		"enable_sms_startstop": ofty_user.enable_sms_startstop,
		"enable_email_new_order": ofty_user.enable_email_new_order,
		"enable_email_startstop": ofty_user.enable_email_startstop
	}
	return JsonResponse(ans)


def about_me(request):
	ans = {
		"username": "anonymous",
		"anonymous": True,
		"city": "Москва",
		"stock-capacity": 0,
		"stock-occupied": 0
	}
	if not request.user.is_anonymous:
		ans["username"] = request.user.username
		ans["anonymous"] = False

		try:
			ofty_user = OftyUser.objects.get(user=request.user)
			ans["stock-capacity"] = ofty_user.stock_size
			ans["stock-occupied"] = len(Unit.objects.filter(owner=request.user, is_deleted=False))
		except OftyUser.DoesNotExist:
			return HttpResponse("its strange, but threre is no such OftyUser", status=500)

	return JsonResponse(ans)


@logged
def get_settings(request):
	django_user = request.user
	uid = django_user.id
	ofty_user = OftyUser.objects.get(user=django_user)
	try:
		wt = OftyUserWorkTime.objects.get(user=django_user)
	except OftyUserWorkTime.DoesNotExist:
		wt = OftyUserWorkTime(user=django_user)
		wt.save()
	bad_guys = BlackListInstance.objects.filter(owner=django_user)
	delivery_cases = DeliveryCase.objects.filter(user=django_user, is_deleted=False)

	ans = {
		"avatar": {
			"big": request.build_absolute_uri(f"/static/user_{uid}/avatar-170.png"),
			"small": request.build_absolute_uri(f"/static/user_{uid}/avatar-71.png"),
		},
		"company": {
			"info": {
				"name": ofty_user.nickname,
				"site": ofty_user.site,
				"city": ofty_user.city.name if ofty_user.city is not None else "",
				"mail": ofty_user.email,
				"phone": ofty_user.phone,
				"phone2": ofty_user.phone2,
				"description": ofty_user.company_description
			},
			"workTime": {
				"mon": {
					"rest": not wt.mon_enable,  # выходной ли
					"start-h": wt.mon_start_h,  # время начала работы
					"start-m": wt.mon_start_m,  # время начала работы
					"fin-h": wt.mon_stop_h,  # время окончания работы
					"fin-m": wt.mon_stop_m,  # время окончания работы
				},
				"tue": {
					"rest": not wt.tue_enable,
					"start-h": wt.tue_start_h,
					"start-m": wt.tue_start_m,
					"fin-h": wt.tue_stop_h,
					"fin-m": wt.tue_stop_m,
				},
				"wed": {
					"rest": not wt.wed_enable,
					"start-h": wt.wed_start_h,
					"start-m": wt.wed_start_m,
					"fin-h": wt.wed_stop_h,
					"fin-m": wt.wed_stop_m,
				},
				"thu": {
					"rest": not wt.thu_enable,
					"start-h": wt.thu_start_h,
					"start-m": wt.thu_start_m,
					"fin-h": wt.thu_stop_h,
					"fin-m": wt.thu_stop_m,
				},
				"fri": {
					"rest": not wt.fri_enable,
					"start-h": wt.fri_start_h,
					"start-m": wt.fri_start_m,
					"fin-h": wt.fri_stop_h,
					"fin-m": wt.fri_stop_m,
				},
				"sat": {
					"rest": not wt.sat_enable,
					"start-h": wt.sat_start_h,
					"start-m": wt.sat_start_m,
					"fin-h": wt.sat_stop_h,
					"fin-m": wt.sat_stop_m,
				},
				"sun": {
					"rest": not wt.sun_enable,
					"start-h": wt.sun_start_h,
					"start-m": wt.sun_start_m,
					"fin-h": wt.sun_stop_h,
					"fin-m": wt.sun_stop_m,
				},
			},
			"notification": {
				"push": ofty_user.enable_push,
				"sound": ofty_user.enable_sound_alert,
				"orderSms": ofty_user.enable_sms_new_order,
				"timeSms": ofty_user.enable_sms_startstop,
				"orderMail": ofty_user.enable_email_new_order,
				"timeMail": ofty_user.enable_email_startstop
			},
			"blackList": [
				{
					"id": bg.id,
					"name": (OftyUser.objects.get(user_id=bg.id)).nickname
				} for bg in bad_guys
			],
			"rent": {
				"address": ofty_user.sklad,  # адрес склада
				"metro": ofty_user.metro,  # ближайшая станция метро
				"description": ofty_user.rent_commentary,  # описание
				"delivery": [
					{
						"id": dc.id,
						"name": dc.name,  # наименование доставки
						"cost": dc.value  # цена
					} for dc in delivery_cases
				]
			}
		}
	}

	return JsonResponse(ans)


@logged
@post_with_parameters("name", "site", "city", "mail", "phone", "phone2", "description")
def save_info(request):
	try:
		django_user = request.user
		ofty_user = OftyUser.objects.get(user=django_user)
		ofty_user.nickname = request.POST["name"]
		ofty_user.site = request.POST["site"]
		ofty_user.city = request.POST["city"]
		ofty_user.email = request.POST["mail"]
		ofty_user.phone = request.POST["phone"]
		ofty_user.phone2 = request.POST["phone2"]
		ofty_user.company_description = request.POST["description"]
		ofty_user.save()

	except OftyUser.DoesNotExist:
		return HttpResponse(f"Data error. OftyUser not found for current user ({django_user.id})", status=500)
	return HttpResponse("OK")


@logged
@post_with_parameters("mon", "tue", "wed", "thu", "fri", "sat", "sun")
def save_work_time(request):
	try:
		django_user = request
		wt = OftyUserWorkTime.objects.get(user=django_user)
		
		wt.mon_enable = not bool(request.POST["mon"]["rest"])
		wt.mon_start_h = request.POST["mon"]["start-h"]
		wt.mon_start_m = request.POST["mon"]["start-m"]
		wt.mon_stop_h = request.POST["mon"]["fin-h"]
		wt.mon_stop_m = request.POST["mon"]["fin-m"]

		wt.tue_enable = not bool(request.POST["tue"]["rest"])
		wt.tue_start_h = request.POST["tue"]["start-h"]
		wt.tue_start_m = request.POST["tue"]["start-m"]
		wt.tue_stop_h = request.POST["tue"]["fin-h"]
		wt.tue_stop_m = request.POST["tue"]["fin-m"]

		wt.wed_enable = not bool(request.POST["wed"]["rest"])
		wt.wed_start_h = request.POST["wed"]["start-h"]
		wt.wed_start_m = request.POST["wed"]["start-m"]
		wt.wed_stop_h = request.POST["wed"]["fin-h"]
		wt.wed_stop_m = request.POST["wed"]["fin-m"]

		wt.thu_enable = not bool(request.POST["thu"]["rest"])
		wt.thu_start_h = request.POST["thu"]["start-h"]
		wt.thu_start_m = request.POST["thu"]["start-m"]
		wt.thu_stop_h = request.POST["thu"]["fin-h"]
		wt.thu_stop_m = request.POST["thu"]["fin-m"]

		wt.fri_enable = not bool(request.POST["fri"]["rest"])
		wt.fri_start_h = request.POST["fri"]["start-h"]
		wt.fri_start_m = request.POST["fri"]["start-m"]
		wt.fri_stop_h = request.POST["fri"]["fin-h"]
		wt.fri_stop_m = request.POST["fri"]["fin-m"]

		wt.sat_enable = not bool(request.POST["sat"]["rest"])
		wt.sat_start_h = request.POST["sat"]["start-h"]
		wt.sat_start_m = request.POST["sat"]["start-m"]
		wt.sat_stop_h = request.POST["sat"]["fin-h"]
		wt.sat_stop_m = request.POST["sat"]["fin-m"]

		wt.sun_enable = not bool(request.POST["sun"]["rest"])
		wt.sun_start_h = request.POST["sun"]["start-h"]
		wt.sun_start_m = request.POST["sun"]["start-m"]
		wt.sun_stop_h = request.POST["sun"]["fin-h"]
		wt.sun_stop_m = request.POST["sun"]["fin-m"]

		wt.save()
	except KeyError:
		return HttpResponse("Wrong data structure", status=500)
	except ValueError:
		return HttpResponse("Wrong data structure (value)", status=500)
	return HttpResponse("OK")


@logged
@post_with_parameters("push", "sound", "orderSms", "timeSms", "orderMail", "timeMail")
def save_notification(request):
	django_user = request.user
	try:
		ofty_user = OftyUser.objects.get(user=django_user)
	except OftyUser.DoesNotExist:
		return HttpResponse(f"there is no OftyUser for user {django_user.id}", status=500)

	ofty_user.enable_push = bool(request.POST["push"])
	ofty_user.enable_sound_alert = bool(request.POST["sound"])
	ofty_user.enable_sms_new_order = bool(request.POST["orderSms"])
	ofty_user.enable_sms_startstop = bool(request.POST["timeSms"])
	ofty_user.enable_email_new_order = bool(request.POST["orderMail"])
	ofty_user.enable_email_startstop = bool(request.POST["timeMail"])
	ofty_user.save()
	return HttpResponse("OK")


def save_blacklist(request):
	return HttpResponse("Method not implemented yet", status=501)


@logged
@post_with_parameters("address", "metro", "description", "delivery")
def save_rent(request):
	django_user = request.user
	try:
		ofty_user = OftyUser.objects.get(user=django_user)
	except OftyUser.DoesNotExist:
		return HttpResponse(f"there is no OftyUser for user {ofty_user.id}", status=500)

	ofty_user.sklad = request.POST["address"]
	ofty_user.metro = request.POST["metro"]
	ofty_user.company_description = request.POST["description"]

	# удалить предыдущие записи
	dcses = DeliveryCase.objects.filter(user=django_user)
	for dc in dcses:
		dc.is_deleted = True
		dc.save()

	upload = json.loads(request.POST["delivery"])
	if type(upload) is not list:
		return HttpResponse("delivery parameter must be valid json array", status=500)

	try:
		for up in upload:
			DeliveryCase.objects.create(
				user=django_user,
				name=up["name"],
				value=up["cost"]
			)
	except KeyError:
		return HttpResponse("wrong data structure", status=500)
	return HttpResponse("OK")
