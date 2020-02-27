from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from account.models import OftyUser, OftyUserWorkTime, DeliveryCase, BlackListInstance
from units.models import Unit
from location.models import City
import json
from PIL import Image, ImageFile
from io import BytesIO
import os
from datetime import datetime, timedelta, timezone
import re
from time import sleep
from shared.methods import post_with_parameters
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import hashlib
import random
from django.conf import settings
import urllib


def get_ofty_user(user):
	# удалить лишние записи в базе данных для этого пользователя
	try:
		ans = OftyUser.objects.get(user=user)
	except OftyUser.DoesNotExist:
		ans = OftyUser.objects.create(user=user)
	except OftyUser.MultipleObjectsReturned:
		OftyUser.objects.filter(user=user).delete()
		ans = OftyUser.objects.create(user=user)
	return ans


# Create your views here.
def logged_and_post(method):
	def inner(request):
		if request.user.is_anonymous:
			return HttpResponse("you must be logged in", status=401)
		if request.method != "POST":
			return HttpResponse("please use POST method", status=500)
		return method(request)
	return inner


def logged(method):
	def inner(request):
		if request.user.is_anonymous:
			return HttpResponse("you must be logged in", status=401)
		return method(request)
	return inner


@post_with_parameters('user', 'password')
def login(request):
	# проверка капчи (если нужно)
	if settings.CAPTCHA['enable'] and 'token' in request.POST:
		params = {
			'secret': settings.CAPTCHA['secret-key'],
			'response': request.POST['token'],
		}
		params = urllib.parse.urlencode(params).encode('ascii')
		try:
			with urllib.request.urlopen('https://www.google.com/recaptcha/api/siteverify', params) as file:
				response = file.read(300)
				try:
					response = json.loads(response)
					if response['success'] and response['action'] == 'register' and response['score'] > 0.5:
						pass  # всё хорошо
					else:
						return HttpResponse("grfo, fckng bot", status=500)
				except ValueError:
					return HttpResponse("captcha error: wrong response from google", status=500)
				except KeyError:
					return HttpResponse("captcha error: invalid google response", status=500)
		except urllib.error.HTTPError:
			return HttpResponse("captcha error: google connection problem", status=500)

	nickname = request.POST['user']
	password = request.POST['password']

	try:
		ofty_user = OftyUser.objects.get(nickname=nickname)
	# except OftyUser.MultipleObjectsReturned:
		# return HttpResponse("Multiaccount error", status=500)
	except OftyUser.DoesNotExist:
		# по никнейму не нашли - попытаемся найти по почте
		try:
			some_user = User.objects.get(email=nickname)
			# нашли - создадим OftyUser и будем подключаться (пытаться по username)
			# попробуем поискать OftyUser
			ofty_user = OftyUser.get_user(some_user)

		except User.DoesNotExist:
			# не нашли - ошибка
			return HttpResponse("login failed", status=500)

	username = ofty_user.user.username

	user = authenticate(username=username, password=password)
	if user is not None:
		django_login(request, user)
		return HttpResponse("OK")
	else:
		return HttpResponse("login failed", status=500)


@logged_and_post
def logout(request):
	django_logout(request)
	return HttpResponse("OK")


def demo(request):
	params = {
		'user_name': request.user.username if not request.user.is_anonymous else "Anonymous",
		"user_id": request.user.id if not request.user.is_anonymous else "X",
		"time": (datetime.now(timezone.utc)-datetime(1970, 1, 1)).total_seconds()
	}
	return render(request, 'account/demo.html', params)


def validate_password(new_password):
	if len(new_password) < 4:
		raise ValueError("password must be at last 4 chars")
	return new_password


@logged_and_post
def password_set(request):
	if "password" not in request.POST:
		return HttpResponse("password not specified", status=500)
	else:
		new_password = request.POST["password"]
		try:
			validate_password(new_password)
		except ValueError as e:
			return HttpResponse(str(e), status=500)
		old_name = request.user.username
		request.user.set_password(new_password)
		request.user.save()
		user = authenticate(request, username=old_name, password=request.POST["password"])
		django_login(request, user)
		return HttpResponse("OK")


@post_with_parameters('email', 'password', 'code')
def password_set_with_code(request):
	try:
		user = User.objects.get(email=request.POST['email'])
		ofty_user = OftyUser.objects.get(user=user)
	except (User.DoesNotExist, OftyUser.DoesNotExist):
		return HttpResponse("not valid user", status=500)

	if ofty_user.verification_code_equals(request.POST['code']):
		new_password = request.POST['password']
		user.set_password(new_password)
		user.save()
		django_login(request, user)
		return HttpResponse("OK")
	else:
		return HttpResponse("code not valid or expired", status=500)


def build_code(ofty_user):
	letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
	code = "".join([letters[random.randint(0, len(letters) - 1)] for i in range(6)])

	# сохранение кода для пользователя
	hash_code = hashlib.md5(code.encode('utf-8'))
	ofty_user.verification_code = hash_code.digest()
	ofty_user.verification_code_until = datetime.utcnow() + timedelta(seconds=60 * 15)
	ofty_user.save()
	return code


@post_with_parameters('email')
def generate_verification_password(request):
	try:
		user = User.objects.get(email=request.POST['email'])
		ofty_user = OftyUser.get_user(user)

		code = build_code(ofty_user)
		params = {'verification_code': code}

		html_message = render_to_string('account/verification_password_email.html', params)
		plain_text = strip_tags(html_message)

		send_mail(
			'код для входа на сайт ofty.ru',
			plain_text,
			"wurka_13@mail.ru",
			(user.email,),
			html_message=html_message,
			fail_silently=False,
			auth_user='wurka_13@mail.ru',
			auth_password='mailPassword'
		)
	except User.DoesNotExist:
		return HttpResponse("no user with this email", status=500)
	except ConnectionRefusedError:
		return HttpResponse("email not send: email server connection refused")

	return HttpResponse("OK")


@post_with_parameters('email', 'password')
def check_verification_password(request):
	try:
		ofty_user = OftyUser.objects.get(user__email=request.POST['email'])
	except OftyUser.DoesNotExist:
		return HttpResponse(f"there is no user with email {request.POST['email']}", status=500)

	if not ofty_user.verification_code_equals(request.POST['password']):
		return HttpResponse('not valid or expired verification code', status=500)

	ans = {
		'code': build_code(ofty_user)
	}
	return JsonResponse(ans)


def validate_nickname(nick):
	# nick - 2-30 символом латиницы или кириллицы
	right = re.match(r'[a-zA-Zа-яА-Я0-9]{2,30}', nick)
	if right:
		if nick != right.group():  # совпадение неполное
			raise ValueError("invalid nickname")
	else:
		raise ValueError('invalid nickname')
	return nick


@post_with_parameters("login", "password", "username")
def new_account(request):
	try:
		User.objects.get(username=request.POST['login'])
		return HttpResponse("login already exists", status=500)
	except User.DoesNotExist:
		new_password = request.POST['password']
		new_login = request.POST['login']
		try:
			nickname = validate_nickname(request.POST['username'])
		except ValueError:
			return HttpResponse("invalid nickname: must be [a-zA-Zа-яА-Я0-9]{2,30}", status=500)

		try:
			validate_password(new_password)
		except ValueError as e:
			return HttpResponse(str(e), status=500)
		new_user = User.objects.create_user(
			username=new_login,
			email=new_login,
			password=new_password)
		new_ofty_user = OftyUser.objects.create(user=new_user, nickname=nickname)

		# создание аватарок
		source = os.path.join(os.getcwd(), 'shared', 'static', 'img', 'shared', 'no_img.png')
		if not os.path.exists(source):
			new_ofty_user.delete()
			new_user.delete()
			return HttpResponse("unable to find avatar source", status=500)
		src = Image.open(source)
		avatar71 = src.resize((71, 71), Image.BILINEAR)
		avatar170 = src.resize((170, 170), Image.BILINEAR)
		src.close()
		d_folder = os.path.join(os.getcwd(), 'user_uploads', f'user_{new_user.id}')
		os.makedirs(d_folder, exist_ok=True)
		d71 = os.path.join(d_folder, 'avatar-71.png')
		d170 = os.path.join(d_folder, 'avatar-170.png')
		avatar71.save(d71, format='PNG')
		avatar71.close()
		avatar170.save(d170, format='PNG')
		avatar170.close()
		src.close()

		return HttpResponse("OK")


@logged_and_post
def save_avatar(request):
	avatar_file_folder = os.path.join("user_uploads", f"user_{request.user.id}")

	os.makedirs(avatar_file_folder, exist_ok=True)

	if "avatar71" not in request.FILES or "avatar170" not in request.FILES:
		return HttpResponse("there is no <avatar71> and <avatar170> in FILES", status=500)

	avatars = [{
			'name': 'avatar71',
			'size': 71,
			'file-name': 'avatar-71.png'
		}, {
			'name': 'avatar170',
			'size': 170,
			'file-name': 'avatar-170.png'
		}
	]

	for avatar in avatars:
		avatar_name = avatar['name']
		avatar_size = avatar['size']
		chunks = request.FILES[avatar_name].chunks()

		file = BytesIO()
		for chunk in chunks:
			file.write(chunk)

		ImageFile.LOAD_TRUNCATED_IMAGES = True

		img = Image.open(file)
		width, height = img.size
		min_size = min(width, height)
		left = width/2.0 - min_size/2.0
		top = height/2.0 - min_size/2.0
		right = width/2.0 + min_size/2.0
		bottom = height/2.0 + min_size/2.0
		img = img.crop((left, top, right, bottom))

		img = img.resize((avatar_size, avatar_size), Image.BICUBIC)
		avatar_file_path = os.path.join(avatar_file_folder, avatar['file-name'])
		img.save(avatar_file_path, "PNG")

	return HttpResponse("OK")


"""
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
"""


def about_me(request):
	ans = {
		"username": "anonymous",
		"anonymous": True,
		"city": "Москва",
		"stock-capacity": 0,
		"stock-occupied": 0
	}
	if not request.user.is_anonymous:
		ans["anonymous"] = False

		ofty_user = get_ofty_user(request.user)
		ans["username"] = ofty_user.nickname
		ans["stock-capacity"] = ofty_user.stock_size
		ans["stock-occupied"] = len(Unit.objects.filter(owner=request.user, is_deleted=False))

	return JsonResponse(ans)


@logged
def get_settings(request):
	django_user = request.user
	uid = django_user.id
	ofty_user = get_ofty_user(django_user)
	try:
		wt = OftyUserWorkTime.objects.get(user=django_user)
	except OftyUserWorkTime.DoesNotExist:
		wt = OftyUserWorkTime(user=django_user)
		wt.save()
	bad_guys = BlackListInstance.objects.filter(owner=django_user)
	delivery_cases = DeliveryCase.objects.filter(user=django_user, is_deleted=False)

	ans = {
		"user": {
			"nickname": ofty_user.nickname,
			"notification": {
				"push": ofty_user.enable_push,
				"sound": ofty_user.enable_sound_alert,
				"orderSms": ofty_user.enable_sms_new_order,
				"timeSms": ofty_user.enable_sms_startstop,
				"orderMail": ofty_user.enable_email_new_order,
				"timeMail": ofty_user.enable_email_startstop
			},
		},
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
			"blackList": [
				{
					"id": bg.id,
					"name": ofty_user.nickname
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


# получить номер телефона из строки, содержащей его
# берутся 11 первых цифр (игнорируются другие символы)
# и из них составляется номер
# если первым шёл "+", то он останется
def build_phone_number(some_string):
	if len(some_string) < 11:
		ans=""  # здесь не может уместиться номер телефона

	digits = "".join(re.findall(r'\d+', some_string))
	if len(digits) < 11:
		ans = ""  # номер телефона не валидный
	else:
		d = digits[:11]
		ans = ""
		if some_string[0] == "+":
			ans += "+"
		ans += f"{d[:4]}-{d[4:7]}-{d[7:9]}-{d[9:11]}"

	if ans == "":
		raise ValueError(f"not valid telephone number: {some_string}")
	return ans


@logged
@post_with_parameters("name", "site", "city", "mail", "phone", "phone2", "description")
def save_info(request):
	django_user = request.user
	sleep(1.0)
	try:
		ofty_user = get_ofty_user(django_user)

		ofty_user.nickname = request.POST["name"]
		filtered = re.match(
			r'^(http://www\.|https://www\.|http://|https://)?[a-z0-9]+([\-.][a-z0-9]+)*\.['
			r'a-z]{2,5}(:[0-9]{1,5})?(/.*)?$', request.POST['site'])
		if filtered is None:
			raise ValueError(f"site not valid: {request.POST['site']}")
		ofty_user.site = filtered.string

		ofty_user.city = City.objects.get(name=request.POST["city"])

		ofty_user.email = request.POST["mail"]

		# значащие цифры но
		ofty_user.phone = build_phone_number(request.POST["phone"])
		ofty_user.phone2 = build_phone_number(request.POST["phone2"])
		ofty_user.company_description = request.POST["description"]
		ofty_user.save()
	except City.DoesNotExist:
		return HttpResponse(f'There is no specified city in base', status=500)
	except ValueError as e:
		return HttpResponse("wrong value: " + str(e), status=500)
	return HttpResponse("OK")


# получить значение часа
def hour(string_value):
	ans = int(string_value)
	if ans < 0 or ans > 23:
		raise ValueError("hour must be 0 to 23")
	return ans


# получить значение минут
def minute(string_value):
	ans = int(string_value)
	if ans < 0 or ans > 59:
		raise ValueError("minutes must be 0 to 59")
	return ans


def flag(json_string_value):
	ans = False
	if type(json_string_value) is str:
		ans = json.loads(json_string_value)
	elif type(json_string_value) is bool:
		return json_string_value
	if type(ans) is not bool:
		return ValueError("value must be <true> or <false>")
	return ans


@logged
@post_with_parameters("mon", "tue", "wed", "thu", "fri", "sat", "sun")
def save_work_time(request):
	try:
		django_user = request.user
		try:
			wt = OftyUserWorkTime.objects.get(user=django_user)
		except OftyUserWorkTime.DoesNotExist:
			wt = OftyUserWorkTime.objects.create(user=django_user)

		days = {
			day: json.loads(request.POST[day]) for day in [
				"mon", "tue", "wed", "thu", "fri", "sat", "sun"
			]
		}
		wt.mon_enable = not flag(days["mon"]["rest"])
		wt.mon_start_h = hour(days["mon"]["start-h"])
		wt.mon_start_m = minute(days["mon"]["start-m"])
		wt.mon_stop_h = hour(days["mon"]["fin-h"])
		wt.mon_stop_m = minute(days["mon"]["fin-m"])

		wt.tue_enable = not flag(days["tue"]["rest"])
		wt.tue_start_h = hour(days["tue"]["start-h"])
		wt.tue_start_m = minute(days["tue"]["start-m"])
		wt.tue_stop_h = hour(days["tue"]["fin-h"])
		wt.tue_stop_m = minute(days["tue"]["fin-m"])

		wt.wed_enable = not flag(days["wed"]["rest"])
		wt.wed_start_h = hour(days["wed"]["start-h"])
		wt.wed_start_m = minute(days["wed"]["start-m"])
		wt.wed_stop_h = hour(days["wed"]["fin-h"])
		wt.wed_stop_m = minute(days["wed"]["fin-m"])

		wt.thu_enable = not flag(days["thu"]["rest"])
		wt.thu_start_h = hour(days["thu"]["start-h"])
		wt.thu_start_m = minute(days["thu"]["start-m"])
		wt.thu_stop_h = hour(days["thu"]["fin-h"])
		wt.thu_stop_m = minute(days["thu"]["fin-m"])

		wt.fri_enable = not flag(days["fri"]["rest"])
		wt.fri_start_h = hour(days["fri"]["start-h"])
		wt.fri_start_m = minute(days["fri"]["start-m"])
		wt.fri_stop_h = hour(days["fri"]["fin-h"])
		wt.fri_stop_m = minute(days["fri"]["fin-m"])

		wt.sat_enable = not flag(days["sat"]["rest"])
		wt.sat_start_h = hour(days["sat"]["start-h"])
		wt.sat_start_m = minute(days["sat"]["start-m"])
		wt.sat_stop_h = hour(days["sat"]["fin-h"])
		wt.sat_stop_m = minute(days["sat"]["fin-m"])

		wt.sun_enable = not flag(days["sun"]["rest"])
		wt.sun_start_h = hour(days["sun"]["start-h"])
		wt.sun_start_m = minute(days["sun"]["start-m"])
		wt.sun_stop_h = hour(days["sun"]["fin-h"])
		wt.sun_stop_m = minute(days["sun"]["fin-m"])

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
	ofty_user = get_ofty_user(django_user)

	try:
		ofty_user.enable_push = flag(request.POST["push"])
		ofty_user.enable_sound_alert = flag(request.POST["sound"])
		ofty_user.enable_sms_new_order = flag(request.POST["orderSms"])
		ofty_user.enable_sms_startstop = flag(request.POST["timeSms"])
		ofty_user.enable_email_new_order = flag(request.POST["orderMail"])
		ofty_user.enable_email_startstop = flag(request.POST["timeMail"])
		ofty_user.save()
		return HttpResponse("OK")
	except ValueError:
		return HttpResponse("Wrong syntax (value)", status=500)


def save_blacklist(request):
	return HttpResponse("Method not implemented yet", status=501)


@logged
@post_with_parameters("address", "metro", "description", "delivery")
def save_rent(request):
	django_user = request.user
	ofty_user = get_ofty_user(django_user)

	max_text_size = 500  # максимальное количество символов в текстовых полях

	ofty_user.sklad = request.POST["address"][:max_text_size]
	ofty_user.metro = request.POST["metro"][:max_text_size]
	ofty_user.rent_commentary = request.POST["description"][:max_text_size]
	ofty_user.save()

	# удалить предыдущие записи
	dcses = DeliveryCase.objects.filter(user=django_user, is_deleted=False)
	for dc in dcses:
		dc.is_deleted = True
		dc.save()

	try:
		upload = json.loads(request.POST["delivery"])
	except json.JSONDecodeError:
		return HttpResponse("Wrong syntax (json decode error)", status=500)
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
		return HttpResponse("Wrong data structure", status=500)
	return HttpResponse("OK")


def get_companies(request):
	owners_ids = set([o.owner.id for o in Unit.objects.all()])
	users = OftyUser.objects.filter(user__id__in=owners_ids).order_by('rating').order_by('nickname')
	ans = [{
		'id': u.id,
		'name': u.nickname,
		'rating': u.rating,
		'positive': u.positive,
		'negative': u.negative,
	} for u in users]

	return JsonResponse(ans, safe=False)


def get_user_list(request):
	all_users = OftyUser.objects.all()
	ans = [{
		'id': user.id,
		'username': user.user.username,
		'nickname': user.nickname,
	} for user in all_users]

	return JsonResponse(ans, safe=False)
