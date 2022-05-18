import json
import app.err_msg as err_msg
import time
from flask import abort

class Validator:

	def check_digit(id, id_name):
		Validator.check_param(id, id_name)
		if not id.isdigit():
			abort(400, err_msg.MUST_INT.format(id_name))
		if int(id) < 1:
			abort(400, err_msg.MUST_POSITIVE_INT.format(id_name))

	def check_json_param(json_str, name):
		Validator.check_param(json_str, name)
		try:
			return json.loads(str)
		except TypeError as e:
			abort(400, err_msg.MUST_JSON.format(name))

	def check_param(param, name):
		if not param:
			abort(400, err_msg.PARAM_EMPTY.format(name))

	def check_time_str(time_str, name):
		Validator.check_param(time_str, name)
		try:
			time.strptime(time_str, '%H:%M:%S')
		except TypeError:
			abort(400, err_msg.WRONG_TIME_FORMAT.format(name))

	def check_list(list_param, name):
		Validator.check_param(list_param, name)
		if type(list_param) is not list:
			abort(400, err_msg.MUST_LIST.format("answer"))
