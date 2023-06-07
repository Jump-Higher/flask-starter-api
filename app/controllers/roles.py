from app import response_handler
from flask import request
from app.models.roles import Roles
from uuid import uuid4
from datetime import datetime
from app import db

def create_role():
    try:
        result = request.json
        select_role = Roles.query.all()

        for i in select_role:
            if result['name'] == i.name:
                return response_handler.bad_request('Role is Exist')
        roles = Roles(id_role = uuid4(),
                      name = result['name'],
                      created_at = datetime.now())
        db.session.add(roles)
        db.session.commit()

        data = {
            "id_roles": roles.id_role,
            "name": roles.name,
            "created_at": roles.created_at
        }
        return response_handler.created(data,"Roles Successfull Created ")
    
    except KeyError as err:
        return response_handler.bad_request(err)
    
    except Exception as err:
        return response_handler.bad_gateway(err)

def read_roles():
    try:
        query_role = Roles.query.all()
        data = []
        for role in query_role:
            dct = {
                "id_role": role.id_role,
                "name": role.name,
                "created_at": role.created_at,
                "updated_at": role.updated_at
            }
            data.append(dct)
            
        return response_handler.ok(data, "tampilin semua role")
    
    except Exception as err:
        return response_handler.bad_gateway("server error")

def edit_role(id):
    try:
        json_body = request.json
        if json_body['name']=="":
            return response_handler.bad_request('name must be filled')
        
        query_roles = Roles.query.all()
        
        exist = False
        for role in query_roles:
            if str(role.id_role) == id:
                exist = True
                break
        
        if not exist:
            return response_handler.not_found('Role not found')
        
        list_role_name = [role.name for role in query_roles]
        print(list_role_name)
        if json_body['name'] in list_role_name:
            return response_handler.bad_request('Role is exist')
        
        role = Roles.query.get(id)
        role.name = json_body['name']
        role.updated_at = datetime.now()
        db.session.commit()

        data = {
            "id_roles": role.id_role,
            "name": role.name,
            "created_at": role.created_at
        }

        return response_handler.ok(data, message="succesfull")

    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    except Exception as err:
        return response_handler.bad_gateway(data="server error")

# def delete_role(id):
#     try:
#         query_roles = Roles.query.all()
#         exist = False
#         for role in query_roles:
#             if str(role.id_role) == id:
#                 exist = True
#                 break

#         if not exist:
#             return response_handler.not_found("Role not found")
        
#         role = Roles.query.get(id)
#         print(role)
#         db.session.delete(role)
#         db.session.commit()

#         return response_handler.ok(None, "Role deleted")
    
#     except Exception as err:
#         return response_handler.bad_gateway("server error")