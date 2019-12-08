from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
import json
from django.core.files.uploadedfile import SimpleUploadedFile


class MyTest(TestCase):
	fixtures = ['location/fixtures/city.json']

	def setUp(self):
		self.test_user = User.objects.create_user("test-user", "test@mail.x", "test-password")
		pass

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

	def test_save_info(self):
		# проверка /account/save-info
		self.client.force_login(self.test_user)
		params = {
			"name": "my nickname",
			"site": "http://www.ya.sru",
			"city": "Москва",
			"mail": "nemail@mail.x",
			"phone": "02",
			"phone2": "03",
			"description": "my description"
		}
		resp = self.client.post(reverse('save-info'), params)
		self.assertEqual(resp.status_code, 200, resp.content)  # запрос прошёл

		resp = self.client.get(reverse('about-me'))
		self.assertEqual(resp.status_code, 200)
		ans = json.loads(resp.content)

		self.assertEqual(ans['city'], 'Москва1')
		self.assertEqual(ans['site'], 'http://www.ya.sru')

		print(ans)
