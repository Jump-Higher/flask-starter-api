import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from app import db
# from app.models import user, regiences

class Address(db.Model):
    __tablename__ = 'tbl_address'
    id_address = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # user = db.relationship('User', backref='tbl_address', uselist=False)
    # id_region = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_regiences.id_region'))

def select_user_address(id):
    query = select(Address).where(Address.id_address == id)
    result = db.session.execute(query)
    id_address = result.scalar()  #return single scalar result
    return id_address

