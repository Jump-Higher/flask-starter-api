from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Db_config, Cloudinary_config
from flask_migrate import Migrate
from flask_cors import CORS
from app.prefix_middleware import PrefixMiddleware
import cloudinary, os

app = Flask(__name__)
app.config.from_object(Db_config)
app.config.from_object(Cloudinary_config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/starter-api/v1')



from app.models import user, address, provinces, regiences


from app import routes
if __name__ == "__main__":
    app.run()