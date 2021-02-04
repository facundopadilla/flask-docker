from flask_restx import Namespace, Resource, fields, abort
from flask_app.models.model_school import School, SchoolSchema
from flask_app.models.model_student import Student
from flask_app.ext.database import db
from .errors import return_error_sql, school_no_exists

# Create name space
api = Namespace("Schools", description="Here are all School endpoints")

# School API Model
school_api_full_model = api.model("School model", {
    "id": fields.Integer(requred=False, description="The ID of school"),
    "name": fields.String(required=True, description="The first name of school", min_length=3, max_length=20),
    "address": fields.String(required=True, description="The last name of school", min_length=3, max_length=20),
    "email": fields.String(required=True, description="The email of school", min_length=10, max_length=30),
    "phone": fields.Integer(required=True, description="The age of school", min=1, max=100, allow_null=False),
    "students": fields.List(fields.String(required=True, description="Students attending this school", allow_null=False))
    })

school_api_model = api.model("School model", {
    "name": fields.String(required=True, description="The first name of school", min_length=3, max_length=20),
    "address": fields.String(required=True, description="The last name of school", min_length=3, max_length=20),
    "email": fields.String(required=True, description="The email of school", min_length=10, max_length=30),
    "phone": fields.Integer(required=True, description="The age of school", min=1, max=100, allow_null=False),
    "students": fields.List(fields.String(required=True, description="Students attending this school", allow_null=False))
    })


# Create resources
@api.route("/")
@api.doc("get_school", model=school_api_full_model)
class SchoolListResource(Resource):

    def get(self):
        """List all schools"""
        schools = School.query.all()
        if schools != []:
            schema = SchoolSchema(many=True)
            return schema.dump(schools)
        return {"message": "List of schools is empty"}, 404
    
    @api.expect(school_api_full_model)
    def post(self):
        """Add new school"""
        try:
            api.payload["students"] = list(map(int, api.payload["students"]))
            students = Student.query.filter(Student.id.in_(set(api.payload["students"]))).all()
            api.payload["students"] = students
            new_school = School(**api.payload)
            db.session.add(new_school)
            db.session.commit()
            schema = SchoolSchema(many=True)
            return {"message":"School was successfully added", "content":[schema.dump(api.payload)]}, 200
        except Exception as e:
            return return_error_sql(e)
            
@api.route("/<int:id>")
@api.param('id', 'the ID of the school you want to obtain')
class SchoolResource(Resource):

    def get(self, id):
        """ Get a school with ID """
        school = School.query.get(id)
        if school is not None:
            schema = SchoolSchema()
            return schema.dump(school)
        return school_no_exists(id)
    
    def delete(self, id):
        """Delete a school by ID"""
        try:
            school = School.query.get(id)
            if school is not None:
                db.session.delete(school)
                db.session.commit()
                schema = SchoolSchema()
                return {"message":"School was successfully added", "content":[schema.jsonify(school)]}
            return school_no_exists(id)
        except Exception as e:
            return return_error_sql(e)

    @api.expect(school_api_model)
    def put(self, id):
        """Put a school by ID"""
        try:
            if len(dict(**api.payload)) == len(school_api_model.keys()):
                school = School.query.filter_by(id=id).update(dict(**api.payload))
                if school:
                    db.session.commit()
                    return {"message":"Updated successfully"}
                return school_no_exists(id)
            else:
                intersection = set(school_api_model.keys()).difference(set(api.payload.keys()))
                return {"message":f"You are missing the following fields to be able to perform the PUT method: {intersection}"}, 400
        except Exception as e:
            return return_error_sql(e)

    @api.expect(school_api_model)
    def patch(self, id):
        """Patch a school by ID"""
        try:
            if api.payload:
                school = School.query.filter_by(id=id).update(dict(**api.payload))
                if school:
                    db.session.commit()
                    return {"message":"Updated successfully"}
                return school_no_exists(id)
            return {"message":f"You must have at least one of all of the following fields: {set(school_api_model.keys())}"}, 400
        except Exception as e:
            return return_error_sql(e)
            
