from flask import render_template, make_response
from flask_restx import Resource

class Index(Resource):
	
	def get(self):
		return make_response(render_template("index.html"))
