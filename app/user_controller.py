from flask_restx import Resource
from flask import request, abort
from flask_login import login_user, logout_user
import json
from app.models import User
from app.validator import Validator
import app.err_msg as err_msg
from app import db
from uuid import uuid4

class UserController(Resource):
		
	def signup():
		body = Validator.check_json(request.data, 'body')
			
		if User.query.filter_by(user_name=body['user_name']).first():
			abort(400, err_msg.USED_USER_NAME.format(body['user_name']))
		
		new_user = User(user_name=body['user_name'], user_passwd=body['user_passwd'])
		db.session.add(new_user)
		db.session.commit()
		return {"result": True}
	
	def login():
		body = Validator.check_json(request.data, 'body')
		
		print(body)
		user = User.query.filter_by(user_name=body['user_name']).first()
		if not user or not user.user_auth(body['user_name'], body['user_passwd']):
			abort(400, err_msg.WRONG_LOGIN_INFO)
		#token = uuid4()
		login_user(user)
		return {"result": True}

	def logout():
		logout_user()
		return {"result":True}	
		
