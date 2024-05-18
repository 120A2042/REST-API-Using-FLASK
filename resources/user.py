from flask.views import MethodView
from flask_smorest import Blueprint ,abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token , get_jwt , jwt_required , create_refresh_token , get_jwt_identity

from db import db
from models import UserModel
from schemas import UserSchema
from Blacklist import BLACKLIST


blueprint = Blueprint("users" , "users" , description = "operation on users")

@blueprint.route("/register")
class UserRegister(MethodView):
    @blueprint.arguments(UserSchema)
    def post(self,user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409 , message = "A provided username already exists")
            
        user = UserModel(username = user_data["username"] , password = pbkdf2_sha256.hash(user_data["password"]))
        db.session.add(user)
        db.session.commit()
        
        return {"message" : "user created successfully"} , 201
    
    
@blueprint.route("/user")
class User(MethodView):
    #for development purpose
    @blueprint.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()
    
    
@blueprint.route("/login")
class UserLogin(MethodView):
    @blueprint.arguments(UserSchema)
    def post(self,user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
            
        if user and pbkdf2_sha256.verify(user_data["password"] , user.password):
            access_token = create_access_token(identity=user.id ,fresh = True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token" : access_token , "refresh_token" : refresh_token} , 200
        
        abort (401 , messsage = "invalid credential")
        
        
@blueprint.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def delete(self):
        jti = get_jwt*["jti"]
        BLACKLIST.add(jti)
        return {"message" : "successfully logged out"} , 200
    
    
@blueprint.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(fresh = True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user , fresh =False)
        
        
        jti = get_jwt()["jti"]
        BLACKLIST.add(jti)
        
        return {"access_token" : new_token} , 200            
            

