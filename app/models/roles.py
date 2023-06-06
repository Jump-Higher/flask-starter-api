from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid

class Roles(db.Model):
    __tablename__ = 'tbl_roles'
    id_role = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    user = db.relationship('User', backref='tbl_roles', uselist=False)
