from app import db, login
from flask_login import UserMixin
import app.err_msg as err_msg
from flask import request, abort
from datetime import datetime

class Challenge(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True, nullable=False)
	question = db.Column(db.Text, nullable=False)
	solution = db.Column(db.Text, nullable=False)
	level = db.Column(db.Integer, nullable=False)
	
	def get(id):
		challenge = Challenge.query.get(id)
		if not challenge:
			abort(404, err_msg.NOT_EXISTING.format('challenge_id'))
		return challenge

	def get_list():
		return Challenge.query.all()
	
	def __repr__(self):
		return '<Challenge {}>'.format(self.name)

class Result(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
	clear_time = db.Column(db.Integer, nullable=False)
	clear_date = db.Column(db.DateTime, nullable=False)

	def top5_by_challenge_id(challenge_id):
		results = Result.query.join(User, Result.user_id==User.id)\
					.join(Challenge, Result.challenge_id==Challenge.id)\
					.add_columns(Challenge.name, User.user_name, Result.clear_time, Result.clear_date)\
					.filter(Challenge.id==challenge_id)\
					.order_by(Result.clear_time.asc()).limit(5)
		if results.count() == 0:
			abort(404, err_msg.NOT_EXISTING.format("challenge_id"))
		return db.session.execute(results)

	def add(user_id, challenge_id, clear_time):
		result = Result(user_id=user_id, challenge_id=challenge_id, clear_time=clear_time,
                clear_date=datetime.now())
		db.session.add(result)
		db.session.commit()

	def __repr__(self):
		return '<Result {}>'.format(str(self.user_id) + str(self.challenge_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String(64), unique=True, nullable=False)
	user_passwd = db.Column(db.Text, nullable=False)

	def user_auth(self, user_name, user_passwd):
		if self.user_name == user_name and self.user_passwd == user_passwd:
			return True
		return False

	def get(id):
		user = User.query.get(int(id))
		if not user:
			abort(404, err_msg.NOT_EXISTING.format('user_id'))
		return user

	def get_by_name(user_name):
		user = User.query.filter_by(user_name=user_name).first()
		if not user:
			abort(404, err_msg.NOT_EXISTING.format('user_name'))
		return user

	def __repr__(self):
		return '<User {}>'.format(self.user_name + self.user_passwd)

@login.user_loader
def load_user(id):
	return User.get(int(id))
