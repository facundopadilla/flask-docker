from flask_app.ext.database import db
from flask_app.ext.schema import ma

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
    email = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(40), nullable=True)
    students = db.relationship('Student', backref="school")

class SchoolSchema(ma.Schema):

    class Meta:
        model = School
        fields = ('id', 'name', 'address', 'email', 'phone', 'students')