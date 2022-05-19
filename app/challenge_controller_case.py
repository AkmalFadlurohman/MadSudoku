import unittest, os
from app import app, db
from app.models import Challenge
import app.models as models
from app.challenge_controller import ChallengeController
import json

class ModelsCase(unittest.TestCase):
		
	def setUp(self):
		basedir = os.path.abspath(os.path.dirname(__file__))
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'test.db')
		self.app = app.test_client() # create a virtual test environment
		db.create_all()

		self.data = []
		self.data.append(Challenge(name="challenge01", level=1, \
						question="[[0,1,7,0,4,5,0,0,0],[0,9,4,0,2,0,8,5,1],[0,6,0,8,0,0,0,7,3],[1,2,0,0,0,0,6,8,0],[5,0,9,1,6,2,0,0,4],[0,4,0,0,0,8,0,1,9],[0,0,2,9,1,3,0,0,0],[0,0,1,6,8,0,0,0,2],[0,0,0,2,0,0,0,9,0]]",\
						solution="[[8,1,7,3,4,5,9,2,6],[3,9,4,7,2,6,8,5,1],[2,6,5,8,9,1,4,7,3],[1,2,3,4,7,9,6,8,5],[5,8,9,1,6,2,7,3,4],[7,4,6,5,3,8,2,1,9],[4,7,2,9,1,3,5,6,8],[9,5,1,6,8,7,3,4,2],[6,3,8,2,5,4,1,9,7]]"))
		self.data.append(Challenge(name="challenge02", level=1, \
						question="[[4,2,7,3,1,9,0,0,8],[0,0,0,0,8,0,0,0,0],[0,8,0,4,0,2,0,0,0],[1,3,0,0,7,0,0,6,5],[0,6,4,8,0,5,1,2,9],[0,0,8,2,6,1,3,0,0],[8,7,1,5,0,0,0,0,0],[0,0,6,0,9,8,7,0,3],[3,4,0,6,2,0,0,0,0]]",\
						solution="[[4,2,7,3,1,9,6,5,8],[9,1,5,7,8,6,4,3,2],[6,8,3,4,5,2,9,1,7],[1,3,2,9,7,4,8,6,5],[7,6,4,8,3,5,1,2,9],[5,9,8,2,6,1,3,7,4],[8,7,1,5,4,3,2,9,6],[2,5,6,1,9,8,7,4,3],[3,4,9,6,2,7,5,8,1]]"))

		for d in self.data:
			db.session.add(d)
		db.session.commit

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_get_challenge(self):
		response = self.app.get('/challenge?id=1')
		
		self.assertEqual(response.status_code, 200)

		challenge = json.loads(response.text)
		self.assertEqual(challenge['name'], self.data[0].name)
		self.assertEqual(challenge['level'], self.data[0].level)
		self.assertEqual(challenge['question'], json.loads(self.data[0].question))
		self.assertEqual(challenge['solution'], json.loads(self.data[0].solution))

	def test_get_challenge_list(self):
		response = self.app.get('/challenge/list')

		self.assertEqual(response.status_code, 200)

		challenge_list = json.loads(response.text)
		self.assertEqual(type(challenge_list), list)
		self.assertEqual(len(challenge_list), 2)
		for i in range(len(challenge_list)):
			self.assertEqual(challenge_list[i]['id'], i+1)
			self.assertEqual(challenge_list[i]['name'], self.data[i].name)
			self.assertEqual(challenge_list[i]['level'], self.data[i].level)
