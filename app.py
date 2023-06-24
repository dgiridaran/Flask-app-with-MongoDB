from cmath import log
from flask import Flask,request
from flask_restful import Resource,Api
from flask_pymongo import PyMongo,ObjectId
from pprint import pprint
from flask_jwt_extended import (JWTManager,create_access_token,get_jwt_identity,jwt_required)
from werkzeug.security import safe_str_cmp,generate_password_hash,check_password_hash
from serializer.register import register
from serializer.login import login
from serializer.template import template
from common.validate import validator
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DB_NAME= os.environ.get('MONGODB_NAME')
DB_URL = os.environ.get('DB_URL')
# from common_functions.serializar import deserializer

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["MONGO_DBNAME"] = DB_NAME
app.config["MONGO_URI"] = DB_URL
mongo = PyMongo(app)
api = Api(app)
jwt = JWTManager(app)



class Register(Resource):


    @classmethod
    def add_user(cls,new_user):
        mongo.db.users.insert_one(new_user)

    @classmethod
    def find_by_email(cls,email=None):
        return mongo.db.users.find_one({"email":email})
    
    @validator(register)
    def post(self):
        data = request.get_json()
        user = {"first_name":data["first_name"],"last_name":data["last_name"], "email":data["email"], "password":generate_password_hash(data["password"])}
        new_user = Register.find_by_email(data['email'])
        if new_user:
            return {"message" : "user with this email, already exists."}, 400
        else:
            try:
                data['password']=generate_password_hash(data['password'])
                Register.add_user(user)
                return {"message" : "User created Sucessfully"},201
            except:
                return {"message" : "Error in creating user, Try again"},500    

class Template(Resource):

    @classmethod
    def add_template(cls,template):
        mongo.db.templates.insert_one(template)

    @jwt_required()
    @validator(template)
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        output = {"template_name":data["template_name"], "subject":data["subject"], "body":data["body"], "user_id":user_id}
        try:
            Template.add_template(output)
            return {"message":"template added successfully"}, 201
        except:
            return {"message":"server error, try again"}, 500
    
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            data = mongo.db.templates
            templates = []
            for template in data.find({"user_id":user_id}):
                templates.append({"id":str(template["_id"]),"template_name":template["template_name"], "subject":template["subject"], "body":template["body"]})
            return {"Output":templates}, 200
        except:
            return {"messsage":"error in geting templates, try again"},500

    
class Templateid(Resource):
    

    @classmethod
    def find_template_by_id(cls,id):
        return mongo.db.templates.find_one({"_id":ObjectId(id)})

    @jwt_required()
    def get(self,template_id):
        data = Templateid.find_template_by_id(template_id)
        try:
            if data:
                output = {"template_name":data["template_name"], "subject":data["subject"],"body":data["body"]}
                return {"Body":output},200
            return {"Body":"template not found"},404
        except:
            return {"message":"error is getting template, try again"},500

    @jwt_required()
    @validator(template)
    def put(self,template_id):
        data = Templateid.find_template_by_id(template_id)
        try:
            if data:
                new_data = request.get_json()
                mongo.db.templates.update_one({"_id":ObjectId(template_id)},{"$set":{"template_name": new_data["template_name"],"subject":new_data["subject"],"body":new_data["body"]}})
                output = Templateid.find_template_by_id(template_id)
                return {"message":"template updated successfully"}, 201
            return {"message":"template not found"},404
        except:
            return {"message":"error in updating template, try again"},500
    
    @jwt_required()
    def delete(self,template_id):
        data = Templateid.find_template_by_id(template_id)
        try:
            if data:
                mongo.db.templates.delete_one({"_id":ObjectId(template_id)})
                return {"message":"template deleted successfully"},200
            return {"message":"template not found"},404
        except:
            return {"message":"error in deleting template, try again"},500


class Templates_sub(Resource):

    @jwt_required()
    def get(self,subject):
        try:
            data = mongo.db.templates
            templates = []
            for template in data.find({"subject":subject}):
                templates.append({"id":str(template["_id"]),"template_name":template["template_name"], "subject":template["subject"], "body":template["body"]})
            return {"Output":templates}, 200
        except:
            return {"messsage":"error in geting templates, try again"},500


class UserLogin(Resource):

    @validator(login)
    def post(self):
        data = request.get_json()
        user = Register.find_by_email(data['email'])
        if not user:
            return {"message":"Pleace insert the correct EmailID."},400
        user_id = str(user['_id'])
        if user and check_password_hash(user["password"],data["password"]):
            access_token = create_access_token(identity=user_id,fresh=True)
            return {
                'access_token':access_token,
            },200
        else:
            return {"message":"Invalid credentials"},401


api.add_resource(Register,'/register')
api.add_resource(Template, '/template')
api.add_resource(UserLogin,'/login')
api.add_resource(Templateid,'/template/<string:template_id>')
api.add_resource(Templates_sub,'/template/<string:subject>')


if __name__ == "__main__":
    app.run(debug=True)