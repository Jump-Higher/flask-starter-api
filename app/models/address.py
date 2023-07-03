from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select
from app import db
from app.models import user, regiences
import uuid


class Address(db.Model):
    __tablename__ = 'tbl_address'
    id_address = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = db.Column(db.String(150))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    #user = db.relationship('User', backref='tbl_address', uselist=False)
    # id_region = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_regiences.id_region'))

def select_user_address(id):
    query = select(Address).where(Address.id_address == id)
    result = db.session.execute(query)
    id_address = result.scalar()
    return id_address

