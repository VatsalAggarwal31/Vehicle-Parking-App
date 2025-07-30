from controllers.database import db
from datetime import datetime, timedelta

utc_now = datetime.now()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(255), nullable=True)

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(255),unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    maximum_number_of_spots = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    parking_spots = db.relationship('ParkingSpot', backref='parking_lot', cascade="all, delete-orphan", lazy='dynamic')

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    vehicle_plate = db.Column(db.String(20), nullable=True)

    reserved_spot_entry = db.relationship('ReservedParkingSpot', backref='parking_spot')

class ReservedParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parking_cost_per_unit_time = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=True)
    vehicle_plate = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    in_time = db.Column(db.DateTime, nullable=False, default=utc_now)
    out_time = db.Column(db.DateTime, nullable=True)

    user = db.relationship(User)
