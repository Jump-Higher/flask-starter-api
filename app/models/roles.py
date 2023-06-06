from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid

class Roles(db.Model):
    __tablename__ = 'tbl_roles'
    id_role = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_user = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_user.id_user'))
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)