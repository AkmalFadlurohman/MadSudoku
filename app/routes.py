# app/routes.py
from app import app
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models import Result, Challenge
import json

ERR_MSG_PARAM_EMPTY = "{} is required."
ERR_MSG_NOT_EXISTING = "non existing {}."
ERR_MSG_MUST_INT = "{} must be an integer."
ERR_MSG_MUST_POSITIVE_INT = "{} must be a positive integer."
ERR_MSG_MUST_JSON = "{} must be a json string."
ERR_MSG_MUST_LIST = "{} must be a list."

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

### get a single challenge data by id
@app.route("/challenge", methods=['GET'])
def get_challenge():
    challenge_id = request.args.get('id')
    flag, msg, code = check_digit(challenge_id, 'challenge_id')
    if not flag:
        return msg, code
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    if challenge is None:
        return ERR_MSG_NOT_EXISTING.format('challenge_id'), 404
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
    flag, msg, code = check_digit(challenge_id, 'challenge_id')
    if not flag:
        return msg, code
    # return results by challenge_id
    results = Result.query.filter_by(challenge_id=challenge_id).all()
    if not results:
        return ERR_MSG_NOT_EXISTING.format("challenge_id"), 404
    result_str = ""
    for r in results:
        result_str += json.dumps({k:r.__dict__[k] \
                if k is not 'clear_date'\
                else r.__dict__[k].strftime("%d/%m/%Y, %H:%M:%S")
                for k in ('id', 'user_name', 'challenge_id', 'clear_time', 'clear_date')})\
                + ','
    result_str = '[' + result_str[:-1] + ']'
    return result_str, 200

@app.route("/result/check", methods=['POST'])
def is_clear():
    # 0. validation
    json_body = request.args.data
    flag, msg, code = validate_claer(json_body)
    if not flag:
        return msg, code

    body_dict = json.loads(body)
    challenge_id = body_dict['challenge_id']
    user_name = body_dict['user_name']
    clear_time = int(body_dict['clear_time'])
    answer = json.loads(body_dic['answer'])
    #flag, msg, code = check_json_param(json_body)
    #if not flag:
    #    return msg, code
    #body_dict = json.loads(json_body)
    #challenge_id = body_dict['challenge_id']
    #flag, msg, code = check_digit(challenge_id, 'challenge_id')
    #if not flag:
    #    return msg, code
    #flag, msg, code = check_param(body_dict['user_name'])
    #answer = body_dict['answer']
    #if type(answer) is not list:
    #    return "param 'asnwer' must be a list.", 400

    # 1. check if the answer of user is correct
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    if not challenge:
        return ERR_MSG_NOT_EXISTING.format("challenge_id"), 400
    solution = json.loads(challenge.solution)
    is_clear = True
    for y in range(9):
        for x in range(9):
            if solution[y][x] != answer[y][x]:
                is_clear = False
                break
        if not is_clear:
            break

    # 2. if it was correct, save the result and reponse true
    Result()
    # 3. if it was incorrect, response false
    return 'not implemented yet'

def validate_clear(body):
    flag, msg, code = check_json_param(body)
    if not flag:
        return False, msg, code
    body_dict = json.loads(body)

    challenge_id = body['challenge_id']
    if not challenge_id:
        return False, ERR_MSG_PARAM_EMPTY.format("challenge_id")
    if type(challenge_id) is not int:
        return False, ERR_MSG_MUST_INT.format("challenge_id"), 400
    
    user_name = body_dict['user_name']
    if not user_name:
        return False, 

    flag, msg, code = check_digit(body_dict['clear_time'], 'clear_time')
    if not flag:
        return False, msg, code

    answer = body_dict['answer']
    if type(answer) is not list:
        return False, ERR_MSG_MUST_LIST.format("asnwer"), 400

    return True, None, None

@app.route("/test", methods=['GET'])
def tset():
    return 'called'

### common functions
def check_digit(id, id_name):
    flag, msg, code = check_param(id, id_name)
    if not flag:
        return flag, msg, code
    if not id.isdigit():
        return False, ERR_MSG_MUST_INT.format(id_name), 400
    if int(id) < 1:
        return False, ERR_MSG_MUST_POSITIVE_INT.format(id_name), 400
    return True, None, None

def check_json_param(json_str, name):
    flag, msg, code = check_param(json_str, name)
    if not flag:
        return flag, msg, code
    if not is_json(json_str):
        return False, ERR_MSG_MUST_JSON.format(name), 400
    return True, None, None

def is_json(str):
    try:
        json.loads(str)
    except ValueError as e:
        return False
    return True

def check_param(param, name):
    if not param:
        return False, ERR_MSG_PARAM_EMPTY.format(name), 400
    return True, None, None
