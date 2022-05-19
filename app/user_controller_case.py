import unittest, os
from app import app, db
from app.models import Result, Challenge, User
import app.models as models
from datetime import datetime
from werkzeug.exceptions import HTTPException
import json

class ModelsCase(unittest.TestCase):
	
	def setUp(self):
		basedir = os.path.abspath(os.path.dirname(__file__))
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'test.db')
		self.app = app.test_client() # create a virtual test environment
		db.create_all()
		self.data = []
		self.data.append(User(user_name="user01", user_passwd="passwd01"))
		self.data.append(User(user_name="user02", user_passwd="passwd02"))

		for d in self.data:
			db.session.add(d)
		db.session.commit

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_signup(self):
		response = self.app.post('/user/signup', data='{"user_name":"user03", "user_passwd":"passwd03"}')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(json.loads(response.text)['result'])

	def test_login(self):
		response = self.app.post('/user/login', data='{"user_name":"user02", "user_passwd":"passwd02"}')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(json.loads(response.text)['result'])

	def test_logout(self):
		response = self.app.post('/user/logout')
		print('-----------', response)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(json.loads(response.text)['result'])
