from app import db

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    question = db.Column(db.Text)
    solution = db.Column(db.Text)
    level = db.Column(db.Integer)

    def __repr__(self):
        return '<Challenge {}>'.format(self.name)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64))
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'))

    def __repr__(self):
        return '<Result {}>'.format(self.user_name + self.challenge_id)
