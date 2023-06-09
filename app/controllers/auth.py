from app import response_handler
from flask import request
from app.models.user import User
from app.hash import hash_password
from app.generate_token import generate_token
from flask_jwt_extended import create_access_token, create_refresh_token


def login():
    try:        
        json_body = request.json        
        if json_body['username'] =="":
            return response_handler.bad_request("username must be filled")
        
        if json_body['password'] =="":
            return response_handler.bad_request("password must be filled")
        
        user = User.query.filter_by(username = json_body['username']).first()
        if not user:
            return response_handler.not_found("user not found")
        
        if hash_password(json_body['password']) != user.password:
            return response_handler.unautorized('login failed')
        
        token = generate_token({"role": "role", "id_user": user.id_user})
        return response_handler.ok(data= token, message='login successful, have a nice day')
    
    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    except Exception as err:
        return response_handler.bad_gateway("server error")