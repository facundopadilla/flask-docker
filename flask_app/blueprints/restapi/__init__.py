import sys
sys.path.append(".")

from flask import Blueprint
from flask_restx import Api, Resource
from flask_app.ext.database import db
from flask_app.models.model_student import Student, StudentSchema
from flask_app.models.model_school import School, SchoolSchema
from .ns_student import api as api_student
from .ns_school import api as api_school

# Here you create the API path
bp = Blueprint("restapi", __name__, url_prefix="/api/v1/")

description = r"""
This is an example of a RESTful API using Flask-RESTX, it consists (actually it was the first thing that came to my mind) of relationships with schools, students, managers and what the rest entails, it is somewhat simple but it would be a complete example using Marshmallow and SQLAlchemy, just add ¯¯\\\_(ツ)_/¯
"""

api = Api(bp, version="Version 1.0 ", title="API Documentation", description=description, doc="/doc")
api.add_namespace(api_student, path="/student")
api.add_namespace(api_school, path="/school")

def init_app(app):
    app.register_blueprint(bp)
