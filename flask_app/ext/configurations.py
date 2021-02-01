from dynaconf import FlaskDynaconf

def init_app(app):
    FlaskDynaconf(app, setting_files=["settings.toml"])