from flask_app.ext.database import db
from flask_app.ext.schema import ma
from .model_student import get_student_schema
from marshmallow import fields

class School(db.Model):
    """ 
    The 'school' model is a OneToMany relationship,
    since each person has an assigned school,
    but a school has many people.
    """

    __tablename__ = "school"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    students = db.relationship('Student', backref="school")

class SchoolSchema(ma.Schema):
    
    class Meta:
        model = School
        include_relationship = True
        fields = ('id', 'name', 'address', 'email', 'phone', 'students')

    students = fields.List(fields.Nested(get_student_schema()))