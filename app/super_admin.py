import os
from app import app, db
from app.hash import hash_password
from uuid import uuid4
from datetime import datetime
from app.models import user, address, provinces, regiences
from app.models.roles import Roles
from app.models.user import User
from app.models.address import Address
 
# make user and super admin
def create_superadmin():
    with app.app_context():
        try:
        # Check if a superuser already exists 
            super_admin = Roles.query.filter_by(name='super_admin').first()
            user = Roles.query.filter_by(name='user').first()
            super_admin_id = uuid4()
            super_admin_address = uuid4()  
            if not super_admin:
                super_admin_role = Roles(id_role=super_admin_id,name='super_admin')
                db.session.add(super_admin_role)
                db.session.commit()

                sa_address = Address(id_address=super_admin_address)
                db.session.add(sa_address)
                db.session.commit()

                superuser = User(
                id_user=uuid4(),
                name='super admin',
                username='super_admin',
                email='super@admin.com',
                password=hash_password('Super@dmin1'),
                status = True,
                picture=os.getenv('DEFAULT_PROFILE_PICTURE'),
                id_address=super_admin_address,
                id_role=super_admin_id
                )
                db.session.add(superuser)
                db.session.commit()
            if not user:
                user_role = Roles(id_role=uuid4(),name='user')
                db.session.add(user_role)
                db.session.commit()
        except:
            pass