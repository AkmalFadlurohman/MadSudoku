from flask_restx import Resource
from flask import request, abort
import app.err_msg
from app.validator import Validator
from app.models import Result, Challenge
import json
from datetime import datetime
from app import db

class ResultHandler(Resource):
	def get(self):
		challenge_id = request.args.get('challenge_id')
		flag, msg, code = Validator.check_digit(challenge_id, 'challenge_id')
		if not flag:
			return msg, code
		# return results by challenge_id
		results = Result.query.filter_by(challenge_id=challenge_id).all()
		if not results:
			abort(404, err_msg.NOT_EXISTING.format("challenge_id"))
		result_str = ""
		for r in results:
			result_str += json.dumps({k:r.__dict__[k] \
					if k is not 'clear_date'\
					else r.__dict__[k].strftime("%d/%m/%Y, %H:%M:%S")
					for k in ('id', 'user_name', 'challenge_id', 'clear_time', 'clear_date')})\
					+ ','
		result_str = '[' + result_str[:-1] + ']'
		return json.loads(result_str)
	
	def post(self):
		# 0. validation
		json_body = request.data
		flag, msg, code = self.validate_clear(json_body)
		if not flag:
			abort(code, msg)
		
		#1. convert json to dictionary and set values
		body_dict = json.loads(json_body)
		challenge_id = body_dict['challenge_id']
		user_name = body_dict['user_name']
		clear_time = int(body_dict['clear_time'])
		answer = body_dict['answer']
		
		# 2. check if the answer of user is correct
		challenge = Challenge.query.filter_by(id=challenge_id).first()
		if not challenge:
			abort(400, err_msg.NOT_EXISTING.format("challenge_id"))
		solution = json.loads(challenge.solution)
		is_clear = True
		for y in range(9):
			for x in range(9):
				if solution[y][x] != answer[y][x]:
					is_clear = False
					break
			if not is_clear:
				break
		
		# 3.if it was incorrect, response false
		if not is_clear:
			return {"clear":False}
		
		# 4.if it was correct, save the result and reponse true
		result = Result(user_name=user_name, challenge_id=challenge_id, clear_time=clear_time,
				clear_date=datetime.now())
		db.session.add(result)
		db.session.commit()
		
		return {"clear":True}

	def validate_clear(self, body):
		flag, msg, code = Validator.check_json_param(body, 'body')
		if not flag:
			return False, msg, code
		body_dict = json.loads(body)
	
		challenge_id = body_dict['challenge_id']
		if challenge_id is None:
			return False, err_msg.PARAM_EMPTY.format("challenge_id"), 400
		if type(challenge_id) is not int:
			return False, err_msg.MUST_INT.format("challenge_id"), 400
		if challenge_id < 1:
			return False, err_msg.MUST_POSITIVE_INT.format("challenge_id"), 400
	
		user_name = body_dict['user_name']
		flag, msg, code = Validator.check_param(user_name, 'user_name')
		if not flag:
			return False, msg, code,
	
		clear_time = body_dict['clear_time']
		if clear_time is None:
			return False, err_msg.PARAM_EMPTY.format("clear_time"), 400
		if type(clear_time) is not int:
			return False, err_msg.MUST_INT.format("clear_time"), 400
		if clear_time < 1:
			return False, err_msg.MUST_POSITIVE_INT.format("clear_time"), 400
	
		answer = body_dict['answer']
		if not answer:
			return False, err_msg.PARAM_EMPTY.format("answer"), 400
		if type(answer) is not list:
			return False, err_msg.MUST_LIST.format("asnwer"), 400
	
		return True, None, None

