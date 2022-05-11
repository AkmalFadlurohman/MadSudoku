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
    if(not challenge_id):
        return "challenge_id is required.", 400
    if(not challenge_id.isdigit()):
        return "challenge_id must be an integer", 400
    if(int(challenge_id) < 1):
        return "challenge_id must be and positive integer", 400
    
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    if(challenge is None):
        return "non existing challenge_id.", 404
    challenge_dict = {k:challenge.__dict__[k] \
                        if(not k in ('question', 'solution')) \
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

@app.route("/test", methods=['GET'])
def tset():
    return 'called'
