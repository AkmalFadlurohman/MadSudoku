# app/routes.py

from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_restx import Resource
from flask_login import login_required
from app.index_controller import IndexController
from app.challenge_controller import ChallengeController
from app.result_controller import ResultController
from app.user_controller import UserController

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
	return IndexController.get_index()
	
@app.route('/challenge', methods=['GET'])
#@login_required
def get_challenge():
	return ChallengeController.get_challenge()

@app.route('/challenge/list', methods=['GET'])
#@login_required
def get_challenge_list():
	return ChallengeController.get_challenge_list()

@app.route('/result', methods=['GET'])
#@login_required
def get_result():
	return ResultController.get_result()

@app.route('/result/check', methods=['POST'])
#@login_required
def check_result():
	return ResultController.check_result()

@app.route('/user/signup', methods=['POST'])
def user_signup():
    return UserController.signup()

@app.route('/user/login', methods=['POST'])
def login():
	return UserController.login()

@app.route('/user/logout', methods=['POST'])
@login_required
def user_logout():
	return UserController.logout()

#class TestApi(Resource):

@app.route('/test', methods=['GET'])
def get_test():
	return 'called'

#api.add_resource(TestApi, '/test')

