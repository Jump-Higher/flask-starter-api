from celery import Celery
from app import app
from app.models import db
from app.models.user import User
from datetime import datetime, timedelta

# Create a Celery instance
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

# Configure Celery
celery.conf.update(app.config)

# Register tasks
@celery.task
def delete_inactive_users():
    with app.app_context():
        expiration_time = datetime.utcnow() - timedelta(hours=1)
        inactive_users = User.query.filter(User.activation_timestamp <= expiration_time).all()

        for user in inactive_users:
            db.session.delete(user)

        db.session.commit()

if __name__ == '__main__':
    celery.start()
