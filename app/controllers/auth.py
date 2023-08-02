from datetime import datetime
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from app import db, response_handler
from app.models.user import User
from app.hash import hash_password
from app.generate_token import generate_token

def login():
    try:        
        json_body = request.json        
        if json_body['username'] =="":
            return response_handler.bad_request("username must be filled")
        
        if json_body['password'] =="":
            return response_handler.bad_request("password must be filled")
        
        user = User.query.filter_by(username = json_body['username']).first()
    
        if not user:
            return response_handler.not_found("Username not found")
        
        if hash_password(json_body['password']) != user.password:
            return response_handler.unautorized('login failed, please check your password again')
        
        if user.status == False:
            return response_handler.unautorized('login failed, please activate your account first or your account is deactivated')
        
        user.last_login = datetime.now()
        db.session.commit()
        token = generate_token({"role": user.id_role, "id_user": user.id_user})
       
        return response_handler.ok(data= token, message='login successful, have a nice day')
    
    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    except Exception as err:
        return response_handler.bad_gateway("server error")