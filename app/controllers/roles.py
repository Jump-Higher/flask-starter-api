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