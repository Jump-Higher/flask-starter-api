import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select
from app import db
from datetime import datetime

class Roles(db.Model):
    __tablename__ = 'tbl_roles'
    id_role = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # user = db.relationship('User', backref='tbl_roles', uselist=False)

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

def admin_role():
    query = select(Roles.id_role).where(Roles.name == 'admin')
    result = db.session.execute(query)
    id_role = result.scalar()
    return id_role
 

