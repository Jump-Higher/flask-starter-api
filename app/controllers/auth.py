from datetime import datetime
from flask import request
# from flask_jwt_extended import decode_token
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
        token = generate_token({"id_user":user.id_user, "role":user.roles.name})
        # decode token
        # print(decode_token(token['token']['access_token']))
        # decode = (decode_token(token['token']['access_token']))
        # print(decode['sub']['role'])
        return response_handler.ok(token, message='login successful, have a nice day')
    
    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    except Exception as err:
        return response_handler.bad_gateway(err)