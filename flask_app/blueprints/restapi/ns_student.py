from flask_restx import Namespace, Resource, fields, abort
from flask_app.models.model_student import Student, StudentSchema
from flask_app.ext.database import db
from re import sub

def return_error_sql(e: str) -> dict:
    error_str = sub(r"[()]","", str(e.__cause__)).split(",")
    error_code = error_str[0]
    error_message = error_str[1].replace(r"\\", "").replace('"', "")
    return {"message":error_message, "code":error_code}

# Create name space
api = Namespace("Students", description="Here are all Student endpoints")

# Student API Model
student_api_model = api.model("Student model", {
    "first_name": fields.String(required=True, description="The first name of student", min_length=3, max_length=20),
    "last_name": fields.String(required=True, description="The last name of student", min_length=3, max_length=20),
    "email": fields.String(required=True, description="The email of student", min_length=10, max_length=30),
    "age": fields.Integer(required=True, description="The age of student", min=1, max=100, allow_null=False),
    "school_id": fields.Integer(required=True, description="The ID of School", allow_null=False)
    })

# Create resources
@api.route("/")
@api.doc("get_student", model=student_api_model)
class StudentListResource(Resource):

    @api.doc("list_students")
    def get(self):
        """List all students"""
        students = Student.query.all()
        if students != []:
            schema = StudentSchema(many=True)
            return schema.dump(students)
        abort(404, "List of students is empty")
    
    @api.expect(student_api_model)
    def post(self):
        """Add new student"""
        try:
            new_student = Student(**api.payload)
            db.session.add(new_student)
            db.session.commit()
            return {"message":"Student was successfully added", "content":[api.payload]}
        except Exception as e:
            return return_error_sql(e)
            
@api.route("/<int:id>")
@api.param('id', 'the ID of the student you want to obtain')
class StudentResource(Resource):

    def get(self, id):
        """ Get a student with ID """
        student = Student.query.get(id)
        if student is not None:
            schema = StudentSchema()
            return schema.dump(student)
        abort(404, "Student doesn't exist")
    
    def delete(self, id):
        """Delete a student by ID"""
        try:
            student = Student.query.get(id)
            if student is not None:
                db.session.delete(student)
                db.session.commit()
                schema = StudentSchema()
                return {"message":"Student was successfully added", "content":[schema.jsonify(student)]}
        except Exception as e:
            return return_error_sql(e)

    @api.expect(student_api_model)
    def put(self, id):
        """Put a student by ID"""
        try:
            if len(dict(**api.payload)) == len(student_api_model.keys()):
                student = Student.query.filter_by(id=id).update(dict(**api.payload))
                if student is not None:
                    db.session.commit()
                    return {"message":"Updated successfully"}
                return {"message": "Student doesn't exist"}
            else:
                intersection = set(student_api_model.keys()).difference(set(api.payload.keys()))
                return {"message":f"You are missing the following fields to be able to perform the PUT method: {intersection}"}
        except Exception as e:
            return return_error_sql(e)

    @api.expect(student_api_model)
    def patch(self, id):
        """Patch a student by ID"""
        try:
            student = Student.query.filter_by(id=id).update(dict(**api.payload))
            if student is not None:
                db.session.commit()
                return {"message":"Updated successfully"}
            return {"message":"Student doesn't exist"}
        except Exception as e:
            return return_error_sql(e)
            
