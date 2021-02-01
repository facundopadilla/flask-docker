from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index_test():
        return "If you see this, Gunicorn works!"

    return app