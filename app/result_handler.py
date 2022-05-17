from flask_restx import Resource
from flask import request, abort
# import app.err_msg
from app import err_msg
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
		results = Result.query.filter_by(challenge_id=challenge_id).order_by(Result.clear_time.asc()).limit(5)
		if not results:
			abort(404, err_msg.NOT_EXISTING.format("challenge_id"))
		result_list=[]
		for r in results:
			dict = r.__dict__
			data = {}
			for k in ('id', 'user_name', 'challenge_id', 'clear_time', 'clear_date'):
				data[k] = dict[k]

			data['clear_date'] = data['clear_date'].strftime("%d/%m/%Y, %H:%M:%S")
			data['clear_time'] = self.convert_from_mil_sec(data['clear_time'])
			result_list.append(data)

#		for r in results:
#			result_str += json.dumps({k:r.__dict__[k] \
#					if k is not 'clear_date'\
#					else r.__dict__[k].strftime("%d/%m/%Y, %H:%M:%S")
#					for k in ('id', 'user_name', 'challenge_id', 'clear_time', 'clear_date')})\
#					+ ','
#		result_str = '[' + result_str[:-1] + ']'
		return result_list

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
		clear_time = self.convert_to_mil_sec(body_dict['clear_time'])
		answer = body_dict['answer']

		# 2. check if the answer of user is correct
		challenge = Challenge.query.filter_by(id=challenge_id).first()
		if not challenge:
			abort(400, err_msg.NOT_EXISTING.format("challenge_id"))
		solution = json.loads(challenge.solution)
		is_clear = True
		for y in range(9):
			for x in range(9):
				if solution[y][x] != int(answer[y][x]):
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
		# if type(challenge_id) is not int:
		# 	return False, err_msg.MUST_INT.format("challenge_id"), 400
		challenge_id = int(challenge_id)
		if challenge_id < 1:
			return False, err_msg.MUST_POSITIVE_INT.format("challenge_id"), 400

		user_name = body_dict['user_name']
		flag, msg, code = Validator.check_param(user_name, 'user_name')
		if not flag:
			return False, msg, code,

		clear_time = body_dict['clear_time']
		if clear_time is None:
			return False, err_msg.PARAM_EMPTY.format("clear_time"), 400
		flag, msg, code = Validator.is_time_str(clear_time, "clear_time")
		if not flag:
			return False, msg, code
		#if type(clear_time) is not int:
		#	return False, err_msg.MUST_INT.format("clear_time"), 400
		#if clear_time < 1:
		#	return False, err_msg.MUST_POSITIVE_INT.format("clear_time"), 400

		answer = body_dict['answer']
		if not answer:
			return False, err_msg.PARAM_EMPTY.format("answer"), 400
		if type(answer) is not list:
			return False, err_msg.MUST_LIST.format("asnwer"), 400

		return True, None, None

	def convert_to_mil_sec(self, time_str):
		hour = 60 * 60 * 1000
		minute = 60 * 1000
		second = 1000
		time = time_str.split(":")
		return int(time[0]) * hour + int(time[1]) * minute + int(time[2]) * second

	def convert_from_mil_sec(self, mil_sec):
		hour = 60 * 60 * 1000
		minute = 60 * 1000
		second = 1000

		h = str(int(mil_sec/hour)).zfill(2)
		m = str(int((mil_sec%hour)/minute)).zfill(2)
		s = str(int((mil_sec%minute)/second)).zfill(2)
		return h+":"+m+":"+s
