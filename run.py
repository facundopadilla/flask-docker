from flask_app.ext import database
from flask_app.ext import schema
from flask_app.ext import commands
from flask_app.ext import configurations
from flask_app.ext import application
from flask_app.blueprints import restapi

def create_run():
    app = application.create_app()
    configurations.init_app(app)
    database.init_app(app)
    commands.init_app(app)
    schema.init_app(app)
    restapi.init_app(app)
    return app


# Create app and factory app
app = create_run()

if __name__ == "__main__":
    app.run()
