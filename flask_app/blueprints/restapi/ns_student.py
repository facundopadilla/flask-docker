from flask_restx import Namespace, Resource, fields
from flask_app.models.model_student import Student, StudentSchema
from flask_app.ext.database import db
from .errors import return_error_sql, student_no_exists

# Create name space
api = Namespace("Students", description="Here are all Student endpoints")

# Student API Model
student_api_full_model = api.model("Student full model", {
    "id": fields.Integer(required=False, description="The ID of student (primary key)"),
    "first_name": fields.String(required=True, description="The first name of student", min_length=3, max_length=20),
    "date_create": fields.DateTime(required=False, description="Date student create"),
    "last_name": fields.String(required=True, description="The last name of student", min_length=3, max_length=20),
    "email": fields.String(required=True, description="The email of student", min_length=10, max_length=30),
    "age": fields.Integer(required=True, description="The age of student", min=1, max=100, allow_null=False),
    "school_id": fields.Integer(required=True, description="The ID of School", allow_null=False)
    })

student_api_model = api.model("Student model", {
    "first_name": fields.String(required=True, description="The first name of student", min_length=3, max_length=20),
    "last_name": fields.String(required=True, description="The last name of student", min_length=3, max_length=20),
    "email": fields.String(required=True, description="The email of student", min_length=10, max_length=30),
    "age": fields.Integer(required=True, description="The age of student", min=1, max=100, allow_null=False),
    "school_id": fields.Integer(required=True, description="The ID of School", allow_null=False)
    })

# Create resources
@api.route("/")
@api.doc(model=student_api_full_model)
class StudentListResource(Resource):

    def get(self):
        """List all students"""
        students = Student.query.all()
        if students != []:
            schema = StudentSchema(many=True)
            return schema.dump(students)
        return {"message":"List of students is empty"}, 404
    
    @api.expect(student_api_model)
    def post(self):
        """Add new student"""
        try:
            new_student = Student(**api.payload)
            db.session.add(new_student)
            db.session.commit()
            return {"message":"Student was successfully added", "content":[api.payload]}, 200
        except Exception as e:
            return return_error_sql(e)
            
@api.route("/<int:id>")
@api.param('id')
@api.doc("Student partial", model=student_api_model)
class StudentResource(Resource):

    def get(self, id):
        """ Get a student with ID """
        student = Student.query.get(id)
        if student is not None:
            schema = StudentSchema()
            return schema.dump(student), 200
        return student_no_exists(id)

    def delete(self, id):
        """Delete a student by ID"""
        try:
            student = Student.query.get(id)
            if student is not None:
                db.session.delete(student)
                db.session.commit()
                schema = StudentSchema()
                return {"message":"Student was successfully deleted", "content":[schema.dump(student)]}, 200
            return student_no_exists(id)
        except Exception as e:
            return return_error_sql(e)

    @api.expect(student_api_model)
    def put(self, id):
        """Put a student by ID"""
        try:
            if len(dict(**api.payload)) == len(student_api_model.keys()):
                student = Student.query.filter_by(id=id).update(dict(**api.payload))
                if student:
                    db.session.commit()
                    return {"message":"Updated successfully"}, 200
                return student_no_exists(id)
            else:
                intersection = set(student_api_model.keys()).difference(set(api.payload.keys()))
                return {"message":f"You are missing the following fields to be able to perform the PUT method: {intersection}"}, 400
        except Exception as e:
            return return_error_sql(e)

    @api.expect(student_api_model)
    def patch(self, id):
        """Patch a student by ID"""
        try:
            if api.payload:
                student = Student.query.filter_by(id=id).update(dict(**api.payload))
                if student:
                    db.session.commit()
                    return {"message":"Updated successfully"}
                return student_no_exists(id)
            return {"message":f"You must have at least one of all of the following fields: {set(student_api_model.keys())}"}, 400
        except Exception as e:
            return return_error_sql(e)
            
