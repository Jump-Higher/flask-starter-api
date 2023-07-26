from flask_mail import Message
from app import mail
from itsdangerous import URLSafeTimedSerializer
from app import os, app, db, secret_key
from flask import jsonify, request, redirect
from app import response_handler,hash_password
from app.models.user import *
from app.models.roles import *
from datetime import datetime
from app.schema.user_schema import UserSchema
from uuid import uuid4
from app.models.user import User

def sendEmail(email,messageBody,subjectBody):
    sendMail = Message(
                 subject = subjectBody,
                 sender = os.getenv('MAIL_USERNAME'),
                 recipients = [email],
                 body = messageBody
            )
    return sendMail
 

def activate_user(activation_token):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(activation_token, max_age=3600)  # Token expires after 1 hour (3600 seconds)
    except:
        return jsonify({'message': 'Invalid or expired activation token.'}), 400

    user = User.query.filter_by(email=email, is_active=False).first()

    if user:
        user.is_active = True
        db.session.commit()
        return redirect('http://localhost:3000/successful_activation')
    else:
        return jsonify({'message': 'User not found or already activated.'}), 400
    
def generate_activation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email)

def register():
    try:
        json_body = request.json
        user_schema = UserSchema()
        
        # checking errors with schema
        errors = user_schema.validate(json_body, partial=('name', 'username', 'email', 'password'))
        if errors:
            return response_handler.bad_request(errors)
        
        # iterasi tbl_user
        list = []
        for i in select_users():
            list.append({
                "username": i.username,
                "email": i.email
            })
        
        # validate if username and email is exist
        for i in list:
            if json_body['username'] == i['username']:
                return response_handler.bad_request('Username is Exist')
            elif json_body['email'] == i['email']:
                return response_handler.bad_request('Email is Exist')
    
        id_address = uuid4()
        date = datetime.now()
        id_role = select_user_role()
        id_user = uuid4()
        activation_token = generate_activation_token(json_body['email'])
        sendMail = sendEmail(json_body['email'],f"Activate Your Account here : {os.getenv('BASE_URL')}activate_user/{activation_token}","Activate Your Account")
        mail.send(sendMail)

        # add to tbl_user
        new_user = User(id_user = id_user, 
                    name = json_body['name'],
                    username = json_body['username'],
                    email = json_body['email'],
                    password = hash_password(json_body['password']),
                    picture = os.getenv('DEFAULT_PROFILE'),
                    id_role = id_role,
                    status = True,
                    id_address = id_address,
                    is_active = False,
                    is_deleted = False,
                    created_at = date,
                    updated_at = date,
                    )
                    
        
        # add to tbl_address
        address = Address(id_address = id_address,
                          created_at = date,
                          updated_at = date)
        
        db.session.add(new_user)
        db.session.add(address)
        db.session.commit()

        user_schema = UserSchema(only=('id_user', 'name', 'username', 'email', 'password', 'created_at'))
        data = user_schema.dump(new_user)

        return response_handler.created(data, 'Check registered email to activate your account')
    
    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))
   