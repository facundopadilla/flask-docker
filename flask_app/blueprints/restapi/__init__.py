import sys
sys.path.append(".")

from flask import Blueprint
from flask_restful import Api
from .resources import StudentResource, SchoolResource

# Here you create the API path
bp = Blueprint("restapi", __name__, url_prefix="/api/v1/")
api = Api(bp)

# Here you add "resources", which are actually the endpoints.
api.add_resource(StudentResource, "/student/")
api.add_resource(SchoolResource, "/school/")

def init_app(app):
    app.register_blueprint(bp)