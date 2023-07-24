from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Db_config, Cloudinary_config, Mail_config
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.prefix_middleware import PrefixMiddleware
from flask_mail import Mail
import cloudinary, os
from app.hash import hash_password

app = Flask(__name__)
app.config.from_object(Cloudinary_config)

app.config.from_object(Db_config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


mail_config = Mail_config
app.config.from_object(Mail_config)
mail = Mail(app)

CORS(app)
app.config["JWT_SECRET_KEY"] = "super-secret" 
jwt = JWTManager(app)
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/starter-api/v1')
  
from app.models import user, address, provinces, regiences
 
from app import app
from uuid import uuid4
from datetime import datetime
from app.models.roles import Roles
from app.models.user import User
from app.models.address import Address



# make user and super admin
with app.app_context():
        try:
        # Check if a superuser already exists 
            super_admin = Roles.query.filter_by(name='super_admin').first()
            user = Roles.query.filter_by(name='user').first()
            super_admin_id = uuid4()
            super_admin_address = uuid4()  
            if not super_admin:
                super_admin_role = Roles(id_role=super_admin_id,name='super_admin',created_at=datetime.now())
                db.session.add(super_admin_role)
                db.session.commit()

                sa_address = Address(id_address=super_admin_address,created_at=datetime.now())
                db.session.add(sa_address)
                db.session.commit()

                superuser = User(
                id_user=uuid4(),
                name='super admin',
                username='super_admin',
                email='super@admin.com',
                password=hash_password('Super@dmin1'),
                status = True,
                is_deleted = False,
                is_active=True,
                created_at=datetime.now(),
                picture=os.getenv('DEFAULT_PROFILE'),
                id_address=super_admin_address,
                id_role=super_admin_id
                )
                db.session.add(superuser)
                db.session.commit()
            if not user:
                user_role = Roles(id_role=uuid4(),name='user',created_at=datetime.now())
                db.session.add(user_role)
                db.session.commit()
        except:
            pass

        


from app import routes
if __name__ == "__main__":
    app.run()