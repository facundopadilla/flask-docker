# Dependency injection with pytest
def test_app_is_created(fixture_create_app):
    assert fixture_create_app.name == "flask_app.ext.application"

def test_run_is_created(fixture_create_run, fixture_create_app):
    assert fixture_create_run.name == fixture_create_app.name