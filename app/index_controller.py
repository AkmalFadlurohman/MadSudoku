from flask import render_template, make_response
from flask_restx import Resource

class IndexController(Resource):
	
	def get_index():
		return make_response(render_template("index.html"))
