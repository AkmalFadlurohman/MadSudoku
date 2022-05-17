from flask_restx import Resource
from flask import request, abort
import json
from app.models import Result, Challenge
from app.validator import Validator
import app.err_msg as err_msg

class ChallengeHandler(Resource):
	def get(self, list=None):
		if list is None:
			return self.get_challenge()
		else:
			return self.get_challenge_list()
		
	def get_challenge(self):
		challenge_id = request.args.get('id')
		flag, msg, code = Validator.check_digit(challenge_id, 'challenge_id')
		if not flag:
			return msg, code
		challenge = Challenge.query.filter_by(id=challenge_id).first()
		if challenge is None:
			abort(400, err_msg.NOT_EXISTING.format('challenge_id'))
		challenge_dict = {k:challenge.__dict__[k] \
						if not k in ('question', 'solution') \
						else json.loads(challenge.__dict__[k]) \
						for k in ('name', 'level', 'question', 'solution')}
		return challenge_dict

	def get_challenge_list(self):
		challenges = Challenge.query.all()
		challenge_list = []
		for c in challenges:
			challenge_list.append({'id':c.id, 'name':c.name, 'level':c.level})
		return challenge_list
	
