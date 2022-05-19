from flask_restx import Resource
from flask import request, abort
import json
from app.models import Result, Challenge
from app.validator import Validator
from flask_login import current_user

class ChallengeController(Resource):
		
	def get_challenge():
		challenge_id = request.args.get('id')
		Validator.check_id(challenge_id, 'challenge_id')
		challenge = Challenge.get(challenge_id)
		challenge_dict = {k:challenge.__dict__[k] \
						if not k in ('question', 'solution') \
						else json.loads(challenge.__dict__[k]) \
						for k in ('name', 'level', 'question', 'solution')}
		return challenge_dict

	def get_challenge_list():
		challenges = Challenge.get_list()
		challenge_list = []
		for c in challenges:
			challenge_list.append({'id':c.id, 'name':c.name, 'level':c.level})
		return json.dumps(challenge_list)	
