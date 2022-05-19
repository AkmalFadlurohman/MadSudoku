# app/routes.py

from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_restx import Resource
#from app.models import Result, Challenge
#import json
#from app.validator import Validator
#import app.err_msg
from flask_login import login_required
from app.index_controller import IndexController
from app.challenge_controller import ChallengeController
from app.result_controller import ResultController
from app.user_controller import UserController

#api.add_resource(Index, "/", "/index")
#api.add_resource(ChallengeHandler, "/challenge")
#api.add_resource(ChallengeHandler, "/challenge/<list>")
#api.add_resource(ResultHandler, "/result")
#api.add_resource(ResultHandler, "/result/check")

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
	return IndexController.get_index()
	
@app.route('/challenge', methods=['GET'])
def get_challenge():
	return ChallengeController.get_challenge()

@app.route('/challenge/list', methods=['GET'])
def get_challenge_list():
	return ChallengeController.get_challenge_list()

@app.route('/result', methods=['GET'])
def get_result():
	return ResultController.get_result()

@app.route('/result/check', methods=['POST'])
def check_result():
	return ResultController.check_result()

@app.route('/user/signup', methods=['POST'])
def user_signup():
    return UserController.signup()

@app.route('/user/login', methods=['POST'])
def user_login():
    return UserController.login()

@app.route('/user/logout', methods=['POST'])
def user_logout():
	return UserController.logout()

#class TestApi(Resource):

@app.route('/test', methods=['GET'])
def get_test():
	return 'called'

#api.add_resource(TestApi, '/test')

