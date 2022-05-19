import unittest, os
from app import app, db
from app.validator import Validator
from datetime import datetime
from werkzeug.exceptions import HTTPException

class ValidatorCase(unittest.TestCase):
	
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_check_id(self):
		with self.assertRaises(HTTPException) as http_error:
			Validator.check_id(0, 'test_id')
		self.assertEqual(http_error.exception.code, 400)
		with self.assertRaises(HTTPException) as http_error:
			Validator.check_id('a', 'test_id')
		self.assertEqual(http_error.exception.code, 400)
		with self.assertRaises(HTTPException) as http_error:
			Validator.check_id('0', 'test_id')
		self.assertEqual(http_error.exception.code, 400)

	def test_check_json(self):
		with self.assertRaises(HTTPException) as http_error:
			Validator.check_json("not json", "test")
		self.assertEqual(http_error.exception.code, 400)
		with self.assertRaises(HTTPException) as http_error:
			Validator.check_json('{"test":}', "test")
		self.assertEqual(http_error.exception.code, 400)

	def test_time_str(self):
		with self.assertRaises(HTTPException) as http_error:
			Validator.check_time_str('00-11-22','test')
		self.assertEqual(http_error.exception.code, 400)

	def test_check_list(self):
		with self.assertRaises(HTTPException) as http_error:
			Validator.check_list(1,'test')
		self.assertEqual(http_error.exception.code, 400)
