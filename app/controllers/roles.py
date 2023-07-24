from app import response_handler
from flask import request
from app.models.roles import Roles, super_admin_role
from uuid import uuid4
from datetime import datetime
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def create_role():
    try:
        super_admin = super_admin_role()
        current_user = get_jwt_identity()
        if current_user['role'] == str(super_admin):
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
        else:
            return response_handler.unautorized("You are not Authorized here")
    
    except KeyError as err:
        return response_handler.bad_request(err)
    
    except Exception as err:
        return response_handler.bad_gateway(err)

@jwt_required()
def read_roles():
    try:
        super_admin = super_admin_role()
        current_user = get_jwt_identity()
        if current_user['role'] == str(super_admin) or 'admin':
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
            return response_handler.ok(data, "")
        return response_handler.unautorized("You are not allowed here")
    except Exception as err:
        return response_handler.bad_gateway(err)

@jwt_required()
def edit_role(id):
    try:
        super_admin = super_admin_role()
        current_user = get_jwt_identity()
        if current_user['role'] == str(super_admin):
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
        return response_handler.unautorized("You are not allowed here")

    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    except Exception as err:
        return response_handler.bad_gateway(data="server error")

@jwt_required()
def list_role():
    try:
        super_admin = super_admin_role()
        current_user = get_jwt_identity()
        if current_user['role'] == str(super_admin) or 'admin':
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 5, type=int )
            total_role = Roles.query.count()
            if not per_page:
                per_page = total_role

            role = Roles.query.order_by(Roles.created_at.desc()).paginate(page = page, per_page = per_page)
            data = []
            for role in role.items:
                data.append({
                    "id_role": role.id_role,
                    "name": role.name,
                    "created_at": role.created_at
                })
            meta = {
                "page": role.page,
                "pages": role.pages,
                "total_count": role.total,
                "prev_page": role.prev_num,
                "next_page": role.next_num,
                "has_prev": role.has_prev,
                "has_next": role.has_next
            }
            return response_handler.ok_with_meta(data,meta)
        return response_handler.unautorized("You are not allowed here")
    except Exception as err:
        return response_handler.bad_gateway(err)
    
@jwt_required()
def bulk_delete_roles():
    try:
        super_admin = super_admin_role()
        current_user = get_jwt_identity()
        if current_user['role'] == str(super_admin):
            json_body = request.json
            id_role_delete = json_body.get('id_role') if json_body else []

            db.session.query(Roles).filter(Roles.id_role.in_(id_role_delete)).delete(synchronize_session=False)
            db.session.commit()
            return response_handler.ok(None, "Delete Roles Successfull")
        return response_handler.unautorized("You are not allowed here")
    except Exception as err:
        return response_handler.bad_gateway(err)


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