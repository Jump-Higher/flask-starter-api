from flask import request
from json_checker import Checker
from app import db, request_mapping, request_struct, response_handler
from app.hash import hash_password
from uuid import uuid4
from datetime import datetime
from app.models.user import *
from app.models.address import Address
from app.models.roles import Roles
from app.response_validator import *
from sqlalchemy import update
import cloudinary,os
from cloudinary.uploader import upload
from app.schema.user_schema import UserSchema
from app.models.roles import select_user_role

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

def create_user():
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
    
        # tbl_address
        id_address = uuid4()
        date = datetime.now()
        id_role = select_user_role()

        # tbl_user
        new_user = User(id_user = uuid4(), 
                    name = json_body['name'],
                    username = json_body['username'],
                    email = json_body['email'],
                    password = hash_password(json_body['password']),
                    picture = os.getenv('DEFAULT_PROFILE'),
                    id_role = id_role,
                    id_address = id_address,
                    is_active = False,
                    created_at = date,
                    updated_at = date,
                    )
        
        address = Address(id_address = id_address,
                          created_at = date,
                          updated_at = date)
        
        db.session.add(new_user)
        db.session.add(address)
        db.session.commit()

        user_schema = UserSchema(only=('id_user', 'name', 'username', 'email', 'password', 'created_at'))
        data = user_schema.dump(new_user)

        return response_handler.created(data, 'User Successfull Created')
    
    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))
    
def read_user(id):
    try:
        id_user = User.query.values(User.id_user)
        exist = False
        for i in id_user:
            if(str(i.id_user) == id):
                exist = True
                break
        
        if not exist:
            return response_handler.not_found('User Not Found')
        
        user = User.query.get(id)
        address = user.address
        role = Roles.query.get(user.id_role)
        
        data = {
            "id_user": user.id_user,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "picture": user.picture,
            "created_at": user.created_at,
            "address": {
                "id_address": address.id_address,
                "address": address.address
            },
            "role":{
                "id_role": role.id_role,
                "role": role.name
            }
            
        }
        return response_handler.ok(data,"")

    except Exception as err:
        return response_handler.bad_gateway(str(err))
    
def update_user(id):
    try:
        id_user = User.query.all()
        exist = False
        for i in id_user:
            if(str(i.id_user) == id):
                exist = True
                break
            
        if not exist:
            return response_handler.not_found('User Not Found')
        
        result = request.form
        # data = request_mapping.update_user(json_body)
        # result = Checker(request_struct.update_user(), soft=True).validate(data)

        validator = validator_update_user(request)
        if not validator.validate():
            errors = validator.errors
            for field in result:
                if field in errors:
                    return response_handler.bad_request(errors['{field}'][0])
            return response_handler.bad_request(errors)
        
        
        user = User.query.filter_by(id_user = id).first()
        address = user.address

        if result['username'] == user.username:
            user.username = result['username']
        else:
            existing_user = User.query.filter_by(username=result['username']).first()
            if existing_user:
                return response_handler.bad_request('Username already exists')

        user.name = result['name']
        user.username = result['username']
        user.email = result['email']
        user.password = hash_password(result['password'])
        address.address = result['address']

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

        db.session.commit()

        data = {
            "id_user": user.id_user,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "picture": user.picture,
            "created_at": user.created_at,
            "address": {
                "id_address": address.id_address,
                "address": address.address
            }
        }
        return response_handler.ok(data, "Your data is updated")

    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))
    
def delete_user(id):
    try:
        id_user = User.query.all()
        exists = False
        for i in id_user:
            if (str(i.id_user) == id):
                exists = True
                break

        if not exists:
            return response_handler.not_found('User Not Found')
        
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        cloudinary.uploader.destroy("api-blog/users/user_"+str(user.id_user))
        return response_handler.ok("","User Successfull Deleted")
    
    except Exception as err:
        return response_handler.bad_gateway(err)

def list_user():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int )
        total_user = User.query.count()
        if not per_page:
            per_page = total_user

        user = User.query.order_by(User.created_at.desc()).paginate(page = page, per_page = per_page)
        data = []
        for i in user.items:
            data.append({
                "id_user": i.id_user,
                "name": i.name,
                "username": i.username,
                "email": i.email,
                "password": i.password,
                "address":{
                    "id_address": i.address.id_address,
                    "address": i.address.address
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
        
