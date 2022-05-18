from flask_restx import Resource
from flask import request, abort
import json
from app.models import User
from app.validator import Validator
import app.err_msg as err_msg

class UserController(Resource):
		
	def sign_up():
		json_body = request.data
		flag, msg, code = 
		User(user_name=)
		pass
	
	def log_in():
		pass

	def validate_user_json(body):
		flag, msg, code = Validator.check_json_param(body, 'body')
		if not flag:
			abort(code, msg)

		body_dict = json.loads(body)
		body_dict['user_name']

