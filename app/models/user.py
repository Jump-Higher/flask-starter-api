import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app import db
from app.models.address import Address
from app.models.roles import Roles

class User(db.Model):
    __tablename__ = 'tbl_user'
    id_user = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    picture = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.String(16))
    status = db.Column(db.Boolean)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    address = db.relationship('Address', backref='tbl_user', uselist=False)
    roles = db.relationship('Roles', backref='tbl_user')
    id_address = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_address.id_address'))
    id_role = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_roles.id_role'))

# object
def select_users():
    select_users = User.query.all()
    return select_users

# query object
def select_user_by_id(id_user):
    select_user = User.query.filter_by(id_user = id_user, is_deleted = False).first()
    return select_user

# object
def select_by_id(id_user):
    select_user = User.query.get(id_user)
    return select_user

def select_user_meta(page, per_page):
        user = User.query.order_by(User.created_at.desc()).paginate(page = page, per_page = per_page)
        return user



