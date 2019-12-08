from django.test import TestCase
from django.urls import reverse


class MyTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		pass

	def test_new_account(self):
		resp = self.client.post(reverse('new-account'), kwargs={"someshit": "x"})
		print(dir(resp))
		self.assertEqual(resp.status_code, 200)

	def test_second(self):
		self.assertEqual(1,1)