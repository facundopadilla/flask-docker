from flask_app.ext.database import db
from flask_app.ext.schema import ma
from datetime import datetime

def get_student_schema():
    return StudentSchema

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

class StudentSchema(ma.Schema):

    class Meta:
        model = Student
        include_fk = True
        fields = ('id', 'date_created', 'first_name', 'last_name', 'email', 'age', 'school_id')
