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
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    address = db.relationship('Address', backref='tbl_user', uselist=False)
