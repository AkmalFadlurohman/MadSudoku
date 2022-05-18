from app import db, login
from flask_login import UserMixin

class Challenge(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True, nullable=False)
	question = db.Column(db.Text, nullable=False)
	solution = db.Column(db.Text, nullable=False)
	level = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return '<Challenge {}>'.format(self.name)

class Result(db.Model):
	id = db.Column(db.Integer, primary_key=True)
#	user_name = db.Column(db.String(64), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
	clear_time = db.Column(db.Integer, nullable=False)
	clear_date = db.Column(db.DateTime, nullable=False)

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

	def __repr__(self):
		return '<User {}>'.format(self.user_name + self.user_passwd)

@login.user_loader
def load_user(id):
	user = User.query.get(int(id))
	print(user)
	return user
