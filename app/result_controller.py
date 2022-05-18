from flask_restx import Resource
from flask import request, abort
import app.err_msg
from app.validator import Validator
from app.models import Result, Challenge, User
import json
from datetime import datetime
from app import db

class ResultController(Resource):

	def get_result():
		challenge_id = request.args.get('challenge_id')
		Validator.check_digit(challenge_id, 'challenge_id')
		# return results by challenge_id
		results = Result.query.join(User, Result.user_id==User.id)\
					.join(Challenge, Result.challenge_id==Challenge.id)\
					.add_columns(Challenge.name, User.user_name, Result.clear_time, Result.clear_date)\
					.filter(Challenge.id==challenge_id)\
					.order_by(Result.clear_time.asc()).limit(5)
		results = db.session.execute(results)
		if not results:
			abort(404, err_msg.NOT_EXISTING.format("challenge_id"))
		result_list=[]
		for r in results:
			dict = r._asdict()
			print(dict)
			data = {}
			for k in ('name', 'user_name', 'clear_time', 'clear_date'):
				data[k] = dict[k]
				
			data['clear_date'] = data['clear_date'].strftime("%d/%m/%Y, %H:%M:%S")
			data['clear_time'] = ResultController.convert_from_mil_sec(data['clear_time'])
			result_list.append(data)
					
		return json.dumps(result_list)

	def check_result():
		# 0. validation
		body_dict = ResultController.validate_clear(request.data)
	
		#1. convert json to dictionary and set values
		challenge_id = body_dict['challenge_id']
		user_name = body_dict['user_name']
		clear_time = ResultController.convert_to_mil_sec(body_dict['clear_time'])
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
		user_id = 1
		result = Result(user_id=user_id, challenge_id=challenge_id, clear_time=clear_time,
				clear_date=datetime.now())
		db.session.add(result)
		db.session.commit()
	
		return {"clear":True}

	def validate_clear(body):
		body_dict = Validator.check_json_param(body, 'body')
		Validator.check_digit(body_dict['challenge_id'], 'challenge_id')
		Validator.check_param(body_dict['user_name'], 'user_name')	
		Validator.check_time_stri(body_dict['clear_time'], 'clear_time')	
		Validator.check_list(body_dict['answer'], 'answer')
		
		return body_dict			

	def convert_to_mil_sec(time_str):
		hour = 60 * 60 * 1000
		minute = 60 * 1000
		second = 1000
		time = time_str.split(":")	
		return int(time[0]) * hour + int(time[1]) * minute + int(time[2]) * second

	def convert_from_mil_sec(mil_sec):
		hour = 60 * 60 * 1000
		minute = 60 * 1000
		second = 1000
		
		h = str(int(mil_sec/hour)).zfill(2)
		m = str(int((mil_sec%hour)/minute)).zfill(2)
		s = str(int((mil_sec%minute)/second)).zfill(2)
		return h+":"+m+":"+s
