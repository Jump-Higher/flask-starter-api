from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid

class User(db.Model):
    __tablename__ = 'tbl_user'
    id_user = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    picture = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.String(16))
    is_active = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    id_address = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_address.id_address'))
    id_role = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_roles.id_role'))

# object
def select_users():
    select_users = User.query.all()
    return select_users

# query object
def select_user_by_id(id_user):
    select_user = User.query.values(User.id_user)
    return select_user

# object
def select_by_id(id_user):
    select_user = User.query.get(id_user)
    return select_user