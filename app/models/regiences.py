from sqlalchemy.dialects.postgresql import UUID
from app import db
from app.models import provinces
import uuid

class Regiences(db.Model):
    __tablename__ = 'tbl_regiences'
    id_region = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    region = db.Column(db.String(20), nullable=False)
    # id_province = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_provinces.id_province'))