from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select
from app import db
import uuid


class Roles(db.Model):
    __tablename__ = 'tbl_roles'
    id_role = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    #user = db.relationship('User', backref='tbl_roles', uselist=False)

def select_user_role():
    query = select(Roles.id_role).where(Roles.name == 'user')
    result = db.session.execute(query)
    id_role = result.scalar()
    return id_role

def super_admin_role():
    query = select(Roles.id_role).where(Roles.name == 'super_admin')
    result = db.session.execute(query)
    id_role = result.scalar()
    return id_role
 

