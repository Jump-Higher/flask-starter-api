from sqlalchemy.dialects.postgresql import UUID
from app import db
from app.models.address import Address
from app.models.roles import Roles
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
    is_deleted = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
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
        # user = User.query.join(User.tbl_address).join(User.tbl_roles).order_by(User.created_at.desc()).paginate(page=page, per_page=per_page)
        # user = User.query.options(db.joinedload('address'), db.joinedload('roles')).order_by(User.created_at.desc()).paginate(page=page, per_page=per_page)
        user = User.query.order_by(User.created_at.desc()).paginate(page = page, per_page = per_page)
        # user = User.query \
        #     .join(User.address) \
        #     .join(User.roles) \
        #     .options(db.contains_eager(User.address), db.contains_eager(User.roles)) \
        #     .order_by(User.created_at.desc()) \
        #     .paginate(page=page, per_page=per_page)
        return user



