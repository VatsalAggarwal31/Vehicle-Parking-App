from flask import current_app as app
from controllers.database import db
from controllers.models import User

def create_table():
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(username='admin').first()
        permanent_user = User.query.filter_by(username='Vatsal').first()
        if not admin:
            admin = User(
                username='admin',
                password='1234',
                full_name='Administrator',
                email='admin@gmail.com',
                phone_number=7217830903,
                address='SCC Heights',
            )
            db.session.add(admin)
        if not permanent_user:
            permanent_user = User(
                username='Vatsal',
                password='1234',
                full_name='Vatsal Aggarwal',
                email='vatsalaggarwal@gmail.com',
                phone_number=7217830903,
                address='SCC Heights',
            )
            db.session.add(permanent_user)

        db.session.commit()
