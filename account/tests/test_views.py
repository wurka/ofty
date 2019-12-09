from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from account.views import build_phone_number


class MyTest(TestCase):
	fixtures = ['location/fixtures/city.json']

	def setUp(self):
		self.test_user = User.objects.create_user("test-user", "test@mail.x", "test-password")
		pass

	def test_login(self):
		# проверка текущего пользователя (должен быть аноним)
		resp = self.client.get(reverse('about-me'))
		ans = json.loads(resp.content)
		self.assertEqual(ans['username'], 'anonymous')
		self.assertEqual(ans['anonymous'], True)

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

	def test_get_settings(self):
		resp = self.client.get(reverse('get-settings'))
		# без логина страница недоступна
		self.assertEqual(resp.status_code, 401)
		# логинимся
		self.client.force_login(self.test_user)
		resp = self.client.get(reverse('get-settings'))
		self.assertEqual(resp.status_code, 200)

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

	def test_build_phone_number(self):
		tests = [
			{
				"src": "+79151234567",
				"ans": "+7915-123-45-67"},
			{
				"src": "+7 915 123 45 67",
				"ans": "+7915-123-45-67"},
			{
				"src": "8 915 123 45 67",
				"ans": "8915-123-45-67"},
			{
				"src": "+7915123456",
				"ans": ""},
			{
				"src": "0123",
				"ans": ""}
		]
		for test in tests:
			bld = build_phone_number(test['src'])
			self.assertEqual(bld, test['ans'])

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
			elif params == 2:
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

	def test_save_notification(self):
		url = reverse('save-notification')
		default_params = {
			"push": "true",
			"sound": "true",
			"orderSms": "true",
			"timeSms": "true",
			"orderMail": "true",
			"timeMail": "true"}

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
