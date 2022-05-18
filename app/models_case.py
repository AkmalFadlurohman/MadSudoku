import unittest, os
from app import app, db
from app.models import Result, Challenge, User
import app.models as models
from datetime import datetime
from werkzeug.exceptions import HTTPException

class ModelsCase(unittest.TestCase):
	
	def setUp(self):
		basedir = os.path.abspath(os.path.dirname(__file__))
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'test.db')
		self.app = app.test_client() # create a virtual test environment
		db.create_all()
		data = []
		data.append(User(user_name="user01", user_passwd="passwd01"))
		data.append(User(user_name="user02", user_passwd="passwd02"))
		data.append(Challenge(name="challenge01", level=1, \
						question="[[0,1,7,0,4,5,0,0,0],[0,9,4,0,2,0,8,5,1],[0,6,0,8,0,0,0,7,3],[1,2,0,0,0,0,6,8,0],[5,0,9,1,6,2,0,0,4],[0,4,0,0,0,8,0,1,9],[0,0,2,9,1,3,0,0,0],[0,0,1,6,8,0,0,0,2],[0,0,0,2,0,0,0,9,0]]",\
						solution="[[8,1,7,3,4,5,9,2,6],[3,9,4,7,2,6,8,5,1],[2,6,5,8,9,1,4,7,3],[1,2,3,4,7,9,6,8,5],[5,8,9,1,6,2,7,3,4],[7,4,6,5,3,8,2,1,9],[4,7,2,9,1,3,5,6,8],[9,5,1,6,8,7,3,4,2],[6,3,8,2,5,4,1,9,7]]"))
		data.append(Challenge(name="challenge02", level=1, \
						question="[[4,2,7,3,1,9,0,0,8],[0,0,0,0,8,0,0,0,0],[0,8,0,4,0,2,0,0,0],[1,3,0,0,7,0,0,6,5],[0,6,4,8,0,5,1,2,9],[0,0,8,2,6,1,3,0,0],[8,7,1,5,0,0,0,0,0],[0,0,6,0,9,8,7,0,3],[3,4,0,6,2,0,0,0,0]]",\
						solution="[[4,2,7,3,1,9,6,5,8],[9,1,5,7,8,6,4,3,2],[6,8,3,4,5,2,9,1,7],[1,3,2,9,7,4,8,6,5],[7,6,4,8,3,5,1,2,9],[5,9,8,2,6,1,3,7,4],[8,7,1,5,4,3,2,9,6],[2,5,6,1,9,8,7,4,3],[3,4,9,6,2,7,5,8,1]]"))
		data.append(Result(user_id=1, challenge_id=1, clear_time=20000, clear_date=datetime.now()))
		data.append(Result(user_id=2, challenge_id=1, clear_time=10000, clear_date=datetime.now()))
		data.append(Result(user_id=1, challenge_id=2, clear_time=30000, clear_date=datetime.now()))
		data.append(Result(user_id=2, challenge_id=2, clear_time=40000, clear_date=datetime.now()))
		data.append(Result(user_id=2, challenge_id=2, clear_time=50000, clear_date=datetime.now()))
		data.append(Result(user_id=2, challenge_id=2, clear_time=60000, clear_date=datetime.now()))
		data.append(Result(user_id=2, challenge_id=2, clear_time=70000, clear_date=datetime.now()))
		data.append(Result(user_id=2, challenge_id=2, clear_time=80000, clear_date=datetime.now()))

		for d in data:
			db.session.add(d)
		db.session.commit

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_challenge_get(self):
		c1 = Challenge.get(1)
		self.assertFalse(c1.name == 'challenge02')
		self.assertTrue(c1.name == 'challenge01')
		with self.assertRaises(HTTPException) as http_error:
			Challenge.get(3)
		self.assertEqual(http_error.exception.code, 404)

	def test_challenge_get_list(self):
		c_list = Challenge.get_list()
		self.assertEqual(len(c_list), 2)

	def test_challeng___repr__(self):
		c1 = Challenge.get(1)
		self.assertEqual(c1.__repr__(), "<Challenge challenge01>")

	def test_result_top5_by_challenge_id(self):
		r_list = Result.top5_by_challenge_id(2)
		result = (('user01','challenge02',30000), ('user02','challenge02',40000), ('user02','challenge02',50000), ('user02','challenge02',60000), ('user02','challenge02',70000), ('user02','challenge02',80000))
		i=0
		for r in r_list:
			d = r._asdict()
			self.assertEqual(d['user_name'], result[i][0])
			self.assertEqual(d['name'], result[i][1])
			self.assertEqual(d['clear_time'], result[i][2])
			i+=1
		with self.assertRaises(HTTPException) as http_error:
			Result.top5_by_challenge_id(3)
		self.assertEqual(http_error.exception.code, 404)

	def test_add(self):
		Result.add(user_id=1, challenge_id=1, clear_time=5000)
		res = (('user01','challenge01',5000), ('user02','challenge01',10000), ('user01','challenge01',20000))
		i = 0
		for r in Result.top5_by_challenge_id(1):
			d = r._asdict()
			self.assertEqual(d['user_name'], res[i][0])
			self.assertEqual(d['name'], res[i][1])
			self.assertEqual(d['clear_time'], res[i][2])
			i+=1

	def test_result___repr__(self):
		r = Result(user_id=5, challenge_id=5, clear_time=500000, clear_date=datetime.now())
		self.assertEqual(r.__repr__(), "<Result 55>")

	def test_user_user_auth(self):
		user = User.get(1)
		self.assertTrue(user.user_auth('user01', 'passwd01'))
		self.assertFalse(user.user_auth('user01', 'passwd02'))

	def test_get(self):
		user = User.get(1)
		self.assertTrue(user.user_name == 'user01')
		self.assertFalse(user.user_name == 'user02')
		with self.assertRaises(HTTPException) as http_error:
			User.get(3)
		self.assertEqual(http_error.exception.code, 404)

	def test_user_get_by_name(self):
		user = User.get_by_name('user01')
		self.assertEqual(user.user_name, 'user01')
		self.assertFalse(user.user_name == 'user02')
		
		with self.assertRaises(HTTPException) as http_error:
			User.get_by_name('user03')
		self.assertEqual(http_error.exception.code, 404)

	def test_user___repr__(self):
		user = User.get(1)
		self.assertEqual(user.__repr__(), "<User user01passwd01>")

	def test_load_user(self):
		user = models.load_user(1)
		self.assertEqual(user.user_name, 'user01')
		self.assertFalse(user.user_name == 'user02')
