from flask_app.ext.database import db
from flask_app.ext.schema import ma
from .model_school import School
from datetime import datetime
import uuid

class Student(db.Model):
    """
    The "person" model is a OneToMany relationship,
    since each person has an assigned school,
    but a school has many people.
    """
    
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)

class StudentSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Student
        include_fk = True
    
    id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    email = ma.auto_field()
    age = ma.auto_field()
    school_id = ma.auto_field()
