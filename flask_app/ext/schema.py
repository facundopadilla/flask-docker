from flask_marshmallow import Marshmallow

ma = Marshmallow()

def init_app(app):
    ma.init_app(app)
