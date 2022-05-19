import json
import app.err_msg as err_msg
import time
from flask import abort
from json import JSONDecodeError

class Validator:

	def check_id(id, id_name):
		Validator.check_param(id, id_name)
		if type(id) is int:
			if id < 1:
				abort(abort(400, err_msg.MUST_POSITIVE_INT.format(id_name)))
			return
		if not id.isdigit():
			abort(400, err_msg.MUST_INT.format(id_name))
		if int(id) < 1:
			abort(400, err_msg.MUST_POSITIVE_INT.format(id_name))

	def check_json(json_str, name, optionals=[]):
		Validator.check_param(json_str, name)
		try:
			dict = json.loads(json_str)
		except JSONDecodeError as e:
			abort(400, err_msg.MUST_JSON.format(name))
		for key in dict:
			if key not in optionals:
				Validator.check_param(dict[key], key)
		return dict

	def check_param(param, name):
		if not param:
			abort(400, err_msg.PARAM_EMPTY.format(name))

	def check_time_str(time_str, name):
		Validator.check_param(time_str, name)
		try:
			time.strptime(time_str, '%H:%M:%S')
		except ValueError:
			abort(400, err_msg.WRONG_TIME_FORMAT.format(name))

	def check_list(list_param, name):
		Validator.check_param(list_param, name)
		if type(list_param) is not list:
			abort(400, err_msg.MUST_LIST.format("answer"))
