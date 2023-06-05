from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid

class Provinces(db.Model):
    __tablename__ = 'tbl_provinces'
    id_province = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    province = db.Column(db.String(20), nullable=False)
    # regiences = db.relationship('Regiences', backref='provinces')
    