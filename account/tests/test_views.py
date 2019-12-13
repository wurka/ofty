from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from account.views import build_phone_number


class MyTest(TestCase):
	fixtures = ['location/fixtures/city.json']

	def page_available(self, url, method="get", params={}):
		if method == "get":
			resp = self.client.get(url, params)
		elif method == "post":
			resp = self.client.post(url, params)
		else:
			raise ValueError("uknown method " + method)
		self.assertEqual(resp.status_code, 200, resp.content)

	def fails(self, url, method, status_code, params={}):
		if method == "get":
			resp = self.client.get(url, params)
		elif method == "post":
			resp = self.client.post(url, params)
		else:
			raise ValueError("uknown method " + method)
		self.assertEqual(resp.status_code, status_code, resp.content)

	def i_am_loggined(self):
		r = self.client.get(reverse('about-me'))
		self.assertEqual(r.status_code, 200, r.content)
		a = json.loads(r.content)
		return not a['anonymous']

	def setUp(self):
		self.test_user = User.objects.create_user("test-user", "test@mail.x", "test-password")
		pass

	def test_login(self):
		# проверка текущего пользователя (должен быть аноним)
		self.assertEqual(self.i_am_loggined(), False)

		# попытка залогиниться
		resp = self.client.post(reverse('login'), {
			'user': 'test-user',
			'password': 'test-password'
		})
		self.assertEqual(resp.status_code, 200)

		# проверка текущего пользователя (должен быть test-user)
		resp = self.client.get(reverse('about-me'))
		self.assertEqual(resp.status_code, 200)
		ans = json.loads(resp.content)
		self.assertEqual(ans['username'], 'test-user')
		self.assertEqual(ans['anonymous'], False)

		# выходим
		self.page_available(reverse('logout'), "post")
		# проверка выхода
		resp = self.client.get(reverse('about-me'))
		self.assertEqual(resp.status_code, 200, resp.content)
		ans = json.loads(resp.content)
		self.assertEqual(self.i_am_loggined(), False)

		# заходим с ошибкой в пароле
		resp = self.client.post(reverse('login'), {
			'user': 'test-user',
			'password': 'XXXXXX'
		})
		self.assertEqual(resp.status_code, 500, resp.content)
		self.assertEqual(self.i_am_loggined(), False)

		# заходим с ошибкой в логине
		resp = self.client.post(reverse('login'), {
			'user': 'uknown-unregistered-user',
			'password': 'wrong-password'
		})
		self.assertEqual(resp.status_code, 500, resp.content)
		self.assertEqual(self.i_am_loggined(), False)

	def test_get_settings(self):
		# без логина страница недоступна
		self.fails(reverse('get-settings'), "get", 401)
		# логинимся
		self.client.force_login(self.test_user)
		self.page_available(reverse('get-settings'), "get")

	def test_avatar(self):
		self.client.force_login(self.test_user)
		resp = self.client.get(reverse('get-settings'))
		self.assertEqual(resp.status_code, 200)
		ans = json.loads(resp.content)
		resp = self.client.get(ans['avatar']['big'])
		self.assertEqual(resp.status_code, 404)
		resp = self.client.get(ans['avatar']['small'])
		self.assertEqual(resp.status_code, 404)

		# загрузка аватара
		with open("./account/tests/image-girl.png", 'rb') as file:
			bts = file.read()
			avatar_file = SimpleUploadedFile('avatar', bts, 'image/png')
			resp = self.client.post(reverse('save-avatar'), {'avatar': avatar_file})
			self.assertEqual(resp.status_code, 200)

		# я не умею проверять static файлы. не проверить =(
		# попытка загрузить ничего
		resp = self.client.post(reverse('save-avatar'))
		self.assertEqual(resp.status_code, 500)

	def test_build_phone_number(self):
		norm_tests = [
			{
				"src": "+79151234567",
				"ans": "+7915-123-45-67"},
			{
				"src": "+7 915 123 45 67",
				"ans": "+7915-123-45-67"},
			{
				"src": "8 915 123 45 67",
				"ans": "8915-123-45-67"}
		]
		fail_tests = [
			"+7915123456", "0123"
		]
		for test in norm_tests:
			bld = build_phone_number(test['src'])
			self.assertEqual(bld, test['ans'])

		for test in fail_tests:
			self.assertRaises(ValueError, build_phone_number, test)

	def test_save_info(self):
		# проверка /account/save-info
		self.client.force_login(self.test_user)

		params_list = [
			{
				"test-number": 0,
				"name": "test nickname 1",
				"site": "http://www.ya.sru",
				"city": "Москва",
				"mail": "test@test.test",
				"phone": "+7 915 123 45 65",
				"phone2": "8(915)123-45-65",
				"description": "my description"},
			{
				"test-number": 1,
				"name": "test nickname 2",
				"site": "http://www.yane.sru",
				"city": "Вязьма",
				"mail": "почта@test2.test2",
				"phone": "+7-915-123-45-65",
				"phone2": "телефон: 8(915)123  45 тире 65",
				"description": "ещё одно описание"
			}, {
				"test-number": 2,
				"name": "test nickname 2",
				"site": "http://www.yane.sru",
				"city": "Город, которого нет",
				"mail": "почта@test2.test2",
				"phone": "+7-915-123-45-65",
				"phone2": "телефон: 8(915)123  45 тире 65",
				"description": "ещё одно описание"
			}
		]
		for params in params_list:
			test_n = params['test-number']

			resp = self.client.post(reverse('save-info'), params)
			if test_n in [0, 1]:
				self.assertEqual(resp.status_code, 200, resp.content)  # запрос прошёл успешно

				resp = self.client.get(reverse('get-settings'))
				self.assertEqual(resp.status_code, 200)
				ans = json.loads(resp.content)

				self.assertEqual(ans['user']['nickname'], params['name'])
				self.assertEqual(ans['company']['info']['city'], params['city'])
				self.assertEqual(ans['company']['info']['site'], params['site'])
				self.assertEqual(ans['company']['info']['mail'], params['mail'])
				self.assertEqual(ans['company']['info']['phone'], '+7915-123-45-65')
				self.assertEqual(ans['company']['info']['phone2'], '8915-123-45-65')
				self.assertEqual(ans['company']['info']['description'], params['description'])
			elif test_n == 2:
				self.assertEqual(resp.status_code, 500)

	def test_save_work_time(self):
		url = reverse('save-work-time')

		default_value = {
			"rest": True,
			"start-h": 0,
			"start-m": 0,
			"fin-h": 0,
			"fin-m": 0
		}
		days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
		params = {
			day: json.dumps(default_value.copy()) for day in days
		}

		# без логина не должно работать
		resp = self.client.post(url, params)
		self.assertEqual(resp.status_code, 401, resp.content)
		# а с логином - должно
		self.client.force_login(self.test_user)
		resp = self.client.post(url, params)
		self.assertEqual(resp.status_code, 200, resp.content)

		# get не должен работать
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 500, resp.content)

		# с отсутствующим хотя бы 1 параметром - не должно работать
		for day in days:
			wrong_params = params.copy()
			wrong_params.pop(day)
			resp = self.client.post(url, wrong_params)
			self.assertEqual(resp.status_code, 500, resp.content)

		# прошлый раз поставили все в default_value, проверим текущие значения
		resp = self.client.get(reverse('get-settings'))
		self.assertEqual(resp.status_code, 200, resp.content)
		ans = json.loads(resp.content)
		for day in days:
			self.assertEqual(ans['company']['workTime'][day], default_value)

		# меняем по 1 дню поочереди, сбрасывая каждый раз в дефолтные перед этим
		another_value = {
			"rest": False,
			"start-h": 1,
			"start-m": 2,
			"fin-h": 3,
			"fin-m": 4
		}
		for day in days:
			resp = self.client.post(url, params)  # go default
			self.assertEqual(resp.status_code, 200, resp.content)
			new_params = params.copy()
			new_params[day] = json.dumps(another_value)
			# отправляем изменённые на этот день параметры
			resp = self.client.post(url, new_params)
			self.assertEqual(resp.status_code, 200, resp.content)
			# проверка значений
			resp = self.client.get(reverse('get-settings'))
			ans = json.loads(resp.content)
			for check_day in days:
				self.assertEqual(
					ans['company']['workTime'][check_day],
					json.loads(new_params[check_day]))

		wrong_values = [
			{
				"rest": "some wrong value",
				"start-h": 24,
				"start-m": 61,
				"fin-h": -1,
				"fin-m": 999
			}, {
				"rest": "100",
				"start-h": 24,
				"start-m": 61,
				"fin-h": -1,
				"fin-m": 999
			}, {
				"totalshit": "over 8000",
			}, {
				"rest": True,
				"start-h": 61,
				"start-m": 10,
				"fin-h": 9,
				"fin-m": 23
			}, {
				"rest": True,
				"start-h": 23,
				"start-m": -5,
				"fin-h": 9,
				"fin-m": 23
			}, {
				"rest": True,
				"start-h": 23,
				"start-m": 3,
				"fin-h": 63,
				"fin-m": 23
			}, {
				"rest": True,
				"start-h": 23,
				"start-m": 3,
				"fin-h": 23,
				"fin-m": 9999
			}
		]
		for wrong_value in wrong_values:
			for day in days:
				params_with_errors = params.copy()
				params_with_errors[day] = json.dumps(wrong_value)
				resp = self.client.post(url, params_with_errors)
				self.assertEqual(resp.status_code, 500, resp.content)

	def test_save_notification(self):
		url = reverse('save-notification')
		default_params = {
			"push": True,
			"sound": True,
			"orderSms": True,
			"timeSms": True,
			"orderMail": True,
			"timeMail": True}

		# не должно работать без логина
		resp = self.client.post(url)
		self.assertEqual(resp.status_code, 401, resp.content)

		self.client.force_login(self.test_user)  # регистрация test-user'a
		# а с логином - должно
		resp = self.client.post(url, default_params)
		self.assertEqual(resp.status_code, 200, resp.content)

		# при этом метод get должен не работать
		resp = self.client.get(url, default_params)
		self.assertEqual(resp.status_code, 500, resp.content)

		# проверка текущего значения (должны были поставится уже)
		resp = self.client.get(reverse('get-settings'))
		self.assertEqual(resp.status_code, 200, resp.content)
		ans = json.loads(resp.content)
		self.assertEqual(ans['user']['notification'], default_params)

		# по очереди установить поля в false и проверить, что поставились
		for option in ["push", "sound", "orderSms", "timeSms", "orderMail", "timeMail"]:
			params = default_params.copy()
			params[option] = "false"
			resp = self.client.post(url, params)
			self.assertEqual(resp.status_code, 200, resp.content)
			resp = self.client.get(reverse('get-settings'))
			self.assertEqual(resp.status_code, 200, resp.content)
			ans = json.loads(resp.content)
			self.assertEqual(ans['user']['notification'], params)

		# ставим хз что
		default_params['push'] = "+"
		default_params['sound'] = "enable"
		resp = self.client.post(url, default_params)
		self.assertEqual(resp.status_code, 500, resp.content)

	def test_save_rent(self):
		# два раза, т.к. при повторном сохранении производится стирание старой инфы
		params = {
			"address": "my address",
			"metro": "Коломенская",
			"description": "Условия аренды",
			"delivery": json.dumps([
				{
					"name": "оленями",
					"cost": 8000},
				{
					"name": "кантованием",
					"cost": 100500}
			])
		}

		for i in range(2):
			# без логина - не должен пройти запрос
			resp = self.client.post(reverse('save-rent'), params)
			self.assertEqual(resp.status_code, 401)

			self.client.force_login(self.test_user)
			# а с логином - должен
			resp = self.client.post(reverse('save-rent'), params)
			self.assertEqual(resp.status_code, 200, resp.content)

			# получить настройки
			resp = self.client.get(reverse('get-settings'))
			self.assertEqual(resp.status_code, 200, resp.content)
			ans = json.loads(resp.content)

			# функция проверки полей delivery
			def deliveries_equals(obj1, obj2):
				for prop in ['address', 'metro', 'description']:
					if obj1[prop] != obj2[prop]:
						return False

				for delivery_case in obj1['delivery']:
					founded = False
					for variant in obj2['delivery']:
						if variant['name'] == delivery_case['name'] and variant['cost'] == delivery_case['cost']:
							founded = True
							break
					if not founded:
						return False
				return True

			sended = params.copy()
			sended['delivery'] = json.loads(params["delivery"])

			self.assertEqual(deliveries_equals(sended, ans['company']['rent']), True, str(params)+"\r\n-------\r\n" + str(ans))
			self.page_available(reverse('logout'), 'post')

		self.client.force_login(self.test_user)
		wrong1 = params.copy()
		wrong1['delivery'] = "[full shit //%}s"
		wrong2 = params.copy()
		wrong2['delivery'] = json.dumps({'this': 'is', 'not': 'array'})
		wrong3 = params.copy()
		wrong3['delivery'] = json.dumps([{'name': 'value', 'xxx': 100}])

		wrong_params = [wrong1, wrong2, wrong3]
		for w in wrong_params:
			self.fails(reverse('save-rent'), 'post', 500, w)

	def test_logout(self):
		# проверка выхода
		self.assertEqual(self.i_am_loggined(), False)
		# без логина - должно не сработать ни POST
		resp = self.client.post(reverse('logout'))
		self.assertEqual(resp.status_code, 401, resp.content)
		# ни GET
		resp = self.client.get(reverse('logout'))
		self.assertEqual(resp.status_code, 401, resp.content)

		# c логином должен сработать только POST
		self.client.force_login(self.test_user)
		self.assertEqual(self.i_am_loggined(), True)
		resp = self.client.get(reverse('logout'))
		self.assertEqual(resp.status_code, 500, resp.content)

		resp = self.client.post(reverse('logout'))
		self.assertEqual(resp.status_code, 200, resp.content)
		self.assertEqual(self.i_am_loggined(), False)

	def test_demo(self):
		self.client.get(reverse('demo'))
		self.assertTemplateUsed('account/demo.html')

	def test_password_set(self):
		url = reverse('password-set')
		resp = self.client.post(url)
		self.assertEqual(resp.status_code, 401)

		params = {
			"password": "new-password"
		}
		resp = self.client.post(url, params)
		self.assertEqual(resp.status_code, 401)

		self.client.force_login(self.test_user)
		resp = self.client.post(url)
		self.assertEqual(resp.status_code, 500, resp.content)
		self.page_available(url, method="post", params=params)
		self.page_available(reverse('logout'), method="post")
		self.assertEqual(self.i_am_loggined(), False)
		self.page_available(reverse('login'), method="post", params={
			"user": "test-user",
			"password": "new-password"
		})

	def test_new_account(self):
		# создание нового аккаунта
		self.page_available(reverse('new-account'), method="post", params={
			"login": "new-login",
			"password": "new-password"
		})

		# залогинится не должно было бы
		self.assertEqual(self.i_am_loggined(), False)
		self.page_available(reverse('login'), method="post", params={
			"user": "new-login",
			"password": "new-password"
		})
		self.assertEqual(self.i_am_loggined(), True)
		self.page_available(reverse('logout'), "post")

		# повторное создание ползователя
		self.fails(reverse('new-account'), "post", 500, {
			"login": "new-login",
			"password": "another-new-password"
		})

	def test_save_blacklist(self):
		self.fails(reverse("save-blacklist"), "post", 501)
