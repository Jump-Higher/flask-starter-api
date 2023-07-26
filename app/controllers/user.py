from flask import request, redirect
from json_checker import Checker
from app import db, request_mapping, request_struct, response_handler, secret_key
from app.hash import hash_password
from uuid import uuid4
from datetime import datetime
from app.models.user import *
from app.models.address import Address, select_user_address
from app.models.roles import Roles
from app.response_validator import *
from sqlalchemy import update
import cloudinary,os
from cloudinary.uploader import upload
from app.schema.user_schema import UserSchema
from app.schema.roles_schema import RolesSchema
from app.schema.address_schema import AddressSchema
from app.models.roles import select_user_role, super_admin_role
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.controllers.send import generate_activation_token


def sendEmail(email,messageBody,subjectBody):
    sendMail = Message(
                 subject = subjectBody,
                 sender = os.getenv('MAIL_USERNAME'),
                 recipients = [email],
                 body = messageBody
            )
    return sendMail

def get_create_user():
    try:
        role = Roles.query.all()

        list_role = []
        for i in role:
            list_role.append({
                "id_role": i.id_role,
                "role": i.name
            })

        return response_handler.ok(list_role,'')
    except Exception as err:
        return response_handler.bad_gateway(str(err))

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

        sendMail = sendEmail(json_body['email'],f"Activate Your Account here : {os.getenv('BASE_URL_BACKEND')}activate_user/{activation_token}","Activate Your Account")

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
   
def read_user(id):
    try:
        #check user is exist or not
        select_user = select_users()
        exist = False
        for i in select_user:
            if(str(i.id_user) == id):
                exist = True
                break
            elif not select_user:
                break
        if not exist:
            return response_handler.not_found('User Not Found')
        # # check user is exist or not
        # select_user = select_user_by_id(id)
        # if select_user is None:
        #     return response_handler.not_found('User Not Found')
        
        # add data user to response
        user = select_by_id(id)
        user_schema = UserSchema()
        data = user_schema.dump(user)

        role = user.roles
        role_schema = RolesSchema()
        role_data = role_schema.dump(role)
        data['role'] = role_data

        address_schema = AddressSchema()
        address = user.address
        address_data = address_schema.dump(address)
        data['address'] = address_data

        return response_handler.ok(data,"")

    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def update_user_role(id):
    try:
        super_admin = super_admin_role()
        current_user = get_jwt_identity()
        if current_user['role'] == str(super_admin):
            json_body = request.json
            user = select_by_id(id)
            if not user:
                return response_handler.not_found("User not found")
            else:
                user.id_role = json_body['id_role']
                user.updated_at = datetime.now()
                db.session.commit()
                return response_handler.ok("", "The user role is changed")
        else:
            return response_handler.unautorized("You are not Authorized here")
    
    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def update_user(id):
    try:
        current_user = get_jwt_identity()
        if current_user['id_user'] == id:
            form_body = request.form
            user_schema = UserSchema()
            address_schema = AddressSchema()
            role_schema = RolesSchema()
            address_data = {'address': form_body['address']}
            # checking errors with schema
            errors = user_schema.validate(form_body)
            address_errors = address_schema.validate(address_data)
            if errors:
                return response_handler.bad_request(errors)
            elif address_errors:
                return response_handler.bad_request(address_errors)
            date = datetime.now()

            # select user by id
            user = select_by_id(id)

            # select address by id
            address = select_user_address(str(user.id_address))
            
            # check username is exist or not
            if form_body['username'] == user.username:
                user.username = form_body['username']
            else:
                existing_user = User.query.filter_by(username=form_body['username']).first()
                if existing_user:
                    return response_handler.bad_request('Username already exists')

            # update user
            user.name = form_body['name']
            user.username = form_body['username']
            user.email = form_body['email']
            user.password = hash_password(form_body['password'])
            user.updated_at = date
            user.phone_number = form_body['phone_number']

            
            # update address
            address.address = form_body['address']
            address.updated_at = date
            if 'picture' in request.files:
                uploadImage = request.files['picture']
                cloudinary_response = cloudinary.uploader.upload(uploadImage,
                                                    folder = "api-blog/users/",
                                                    public_id = "user_"+str(user.id_user),
                                                    overwrite = True,
                                                    width = 250,
                                                    height = 250,
                                                    grafity = "auto",
                                                    radius = "max",
                                                    crop = "fill"
                                                    ) 
                user.picture = cloudinary_response["url"]
            elif 'picture' not in request.files:
                user.picture = user.picture

            db.session.commit()

            return response_handler.ok("", "Your data is updated")
        else:
            return response_handler.bad_request("You can't change another people account")

    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def delete_user(id):
    try:
        current_user = get_jwt_identity()
        if current_user['id_user'] == id:
            id_user = User.query.all()
            exists = False
            for i in id_user:
                if (str(i.id_user) == id):
                    exists = True
                    break

            if not exists:
                return response_handler.not_found('User Not Found')
            
            user = select_by_id(id)
            user.is_deleted = True

            db.session.commit()
            # cloudinary.uploader.destroy("api-blog/users/user_"+str(user.id_user))
            return response_handler.ok("","User Successfull Deleted")
        else:
            return response_handler.bad_request("You can't delete another people account")

    
    except Exception as err:
        return response_handler.bad_gateway(err)

def list_user():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int )
        total_user = User.query.count()
        if not per_page:
            per_page = total_user

       
        total_page = (total_user-1+per_page)//per_page
        if (page <= 0 or page > total_page ):
            response= {
                "code": "404",
                "status": "NOT_FOUND",
                "errors": "page cannot negative value or more than total page",
                "data": {
                    "total_page": total_page
                }
            }
            return response_handler.not_found(response)

        user = User.query.order_by(User.created_at.desc()).paginate(page = page, per_page = per_page)
        data = []
        for i in user.items:
            data.append({
                "id_user": i.id_user,
                "name": i.name,
                "username": i.username,
                "email": i.email,
                "password": i.password,
                "picture" : i.picture,
                "phone_number" : i.phone_number,
                "is_active" : i.is_active,
                "is_deleted" : i.is_deleted,
                "created_at" : i.created_at,
                "updated_at" : i.updated_at,
                "address":{
                    "id_address": i.address.id_address,
                    "address": i.address.address
                },
                "role":{
                    "id_role": i.roles.id_role,
                    "role": i.roles.name
                }
            })
        meta = {
            "page": user.page,
            "pages": user.pages,
            "total_count": user.total,
            "prev_page": user.prev_num,
            "next_page": user.next_num,
            "has_prev": user.has_prev,
            "has_next": user.has_next
        }
        return response_handler.ok_with_meta(data,meta)
    except Exception as err:
        return response_handler.bad_gateway(err)
    
def activate_user(activation_token):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(activation_token, max_age=3600)  # Token expires after 1 hour (3600 seconds)
    except Exception as err:
        return response_handler.bad_gateway(err)
    
    user = User.query.filter_by(email=email, is_active=False).first()

    if user:
        user.is_active = True
        db.session.commit()
        return redirect('http://localhost:3000/successful_activation')
    else: 
        return response_handler.bad_request("Your account is already activated or token is expired")
 
@jwt_required()      
def deactivate_user(id):
    try:
        super_admin = super_admin_role()
        current_user = get_jwt_identity()
        if current_user['role'] == str(super_admin):
            user = select_by_id(id)
            user.status = False
            db.session.commit()
            return response_handler.ok("", f"{user.username} success to deactivate")
        return response_handler.unautorized("You are not allowed here")
    except Exception as err:
        return response_handler.bad_gateway(err)
