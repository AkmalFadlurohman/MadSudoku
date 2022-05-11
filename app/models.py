from app import db

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
    user_name = db.Column(db.String(64), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    clear_time = db.Column(db.Integer, nullable=False)
    clear_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Result {}>'.format(self.user_name + str(self.challenge_id))
