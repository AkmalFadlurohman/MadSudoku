# app/routes.py

from app import api
#from flask import render_template, request, flash, redirect, url_for
from flask_restx import Resource
#from app.models import Result, Challenge
#import json
#from app.validator import Validator
#import app.err_msg
from app.index import Index
from app.challenge_handler import ChallengeHandler
from app.result_handler import ResultHandler

api.add_resource(Index, "/", "/index")
api.add_resource(ChallengeHandler, "/challenge")
api.add_resource(ChallengeHandler, "/challenge/<list>")
api.add_resource(ResultHandler, "/result")
api.add_resource(ResultHandler, "/result/check")

class TestApi(Resource):
	def get():
		return 'called'

api.add_resource(TestApi, '/test')

