from flask_app.ext.database import db
from flask_app.models.model_student import Student, StudentSchema
from flask_app.models.model_school import School, SchoolSchema
from flask_restful import Resource, abort
from flask import request, jsonify

def abort_204():
    return abort(404, message="No data loaded in table, you should add to start working, right? :)")

class StudentResource(Resource):

    def get(self):
        """Gets all students"""
        students = Student.query.all()
        if students != []:
            schema = StudentSchema(many=True)
            return schema.dump(students)
        abort_204()
    
    def post(self, *args, **kwargs):
        print("HOLA ---------------------")
        return jsonify({"message":"hola"})

class SchoolResource(Resource):

    def get(self):
        """Gets all schools"""
        schools = School.query.all()
        if schools != []:
            schema = SchoolSchema(many=True)
            return schema.dump(schools)
        abort_204()
