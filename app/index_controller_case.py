import unittest, os
from app import app

class IndexControllerCase(unittest.TestCase):
	
	def setUp(self):
		self.app = app.test_client()

	def tearDown(self):
		pass

	def test_check_id(self):
		response = self.app.get('/index')
		self.assertEqual(response.status_code, 200)
