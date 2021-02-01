from flask_app.ext.database import db
from flask_app.models.model_student import Student
from flask_app.models.model_school import School
from faker import Faker

f = Faker()

def init_app(app):
    @app.cli.command("create_db")
    def create_db():
        db.create_all()
    
    @app.cli.command("drop_db")
    def drop_db():
        db.drop_all()

    @app.cli.command("add_student")
    def add_student_to_db():
        data = [
            Student(
                first_name=f.first_name(),
                last_name=f.last_name(),
                email=f.email(),
                age=str(f.pyint(min_value=6, max_value=100))
            )
        ]
        db.session.bulk_save_objects(data)
        db.session.commit()
        return Student.query.all()
    
    @app.cli.command("add_school")
    def add_school_to_db():
        data = [
            School(
                name=f.company(),
                address=f.address(),
                email=f.email(),
                phone=f.phone_number()
            )
        ]
        db.session.bulk_save_objects(data)
        db.session.commit()
        return School.query.all()
    
    app.cli.add_command(create_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(add_student_to_db)
    app.cli.add_command(add_school_to_db)