# app/routes.py
from app import app
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models import Result, Challenge
import json

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

### get a single challenge data by id
@app.route("/challenge", methods=['GET'])
def get_challenge():
    challenge_id = request.args.get('id')
    flag, msg, code = check_id(challenge_id, 'challenge_id')
    if not flag:
        return msg, code
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    if challenge is None:
        return "non existing challenge_id.", 404
    challenge_dict = {k:challenge.__dict__[k] \
                        if not k in ('question', 'solution') \
                        else json.loads(challenge.__dict__[k]) \
                        for k in ('name', 'level', 'question', 'solution')}
    print(challenge_dict)
    return json.dumps(challenge_dict), 200

@app.route("/challenge/list", methods=['GET'])
def get_challenge_list():
    challenges = Challenge.query.all()
    challenge_list = []
    for c in challenges:
        challenge_list.append({'id':c.id, 'name':c.name, 'level':c.level})
    return json.dumps(challenge_list)

@app.route("/result", methods=['GET'])
def get_result():
    challenge_id = request.args.get('challenge_id')
    flag, msg, code = check_id(challenge_id, 'challenge_id')
    if not flag:
        return msg, code
    # return results by challenge_id
    results = Result.query.filter_by(challenge_id=challenge_id).all()
    if not results:
        return "non existing challenge_id", 404
    result_str = ""
    for r in results:
        result_str += json.dumps({k:r.__dict__[k] \
                if k is not 'clear_date'\
                else r.__dict__[k].strftime("%d/%m/%Y, %H:%M:%S")
                for k in ('id', 'user_name', 'challenge_id', 'clear_time', 'clear_date')})
    return result_str, 200

@app.route("/result/check", methods=['POST'])
def is_clear():
    # 1. check if the answer of user is correct
    # 2. if it was correct, save the result and reponse true
    # 3. if it was incorrect, response false
    return 'not implemented yet'

@app.route("/test", methods=['GET'])
def tset():
    return 'called'

### common functions
def check_id(id, id_name):
    if not id:
        return False, "{} is required.".format(id_name), 400
    if not id.isdigit():
        return False, "{} must be an integer".format(id_name), 400
    if int(id) < 1:
        return False, "{} must be and positive integer".format(id_name), 400
    return True, None, None
