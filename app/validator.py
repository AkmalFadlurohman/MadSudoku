import json
import app.err_msg as err_msg
import time

class Validator:

	@classmethod
	def check_digit(self, id, id_name):
		flag, msg, code = self.check_param(id, id_name)
		if not flag:
			return flag, msg, code
		if not id.isdigit():
			return False, err_msg.MUST_INT.format(id_name), 400
		if int(id) < 1:
			return False, err_msg.MUST_POSITIVE_INT.format(id_name), 400
		return True, None, None

	@classmethod
	def check_json_param(self, json_str, name):
		flag, msg, code = self.check_param(json_str, name)
		if not flag:
			return flag, msg, code
		if not self.is_json(json_str):
			return False, err_msg.MUST_JSON.format(name), 400
		return True, None, None

	@classmethod
	def is_json(self, str):
		try:
			json.loads(str)
		except ValueError as e:
			return False
		return True

	@classmethod
	def check_param(self, param, name):
		if not param:
			return False, err_msg.PARAM_EMPTY.format(name), 400
		return True, None, None

	@classmethod
	def is_time_str(self, time_str, name):
		try:
			time.strptime(time_str, '%H:%M:%S')
			return True, None, None
		except TypeError:
			return False, err_msg.WRONG_TIME_FORMAT.format(name) ,400
