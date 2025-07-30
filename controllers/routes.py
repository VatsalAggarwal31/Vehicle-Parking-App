import math
from app import app
from flask import render_template, request, redirect, flash, url_for, session
from controllers.database import db
from controllers.models import User, ParkingLot, ParkingSpot, ReservedParkingSpot
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_parking_spots_chart():
    lst_of_parking_lots_name = []
    lst_of_parking_lots_available_count = []
    lst_of_parking_lots_occupied_count = []

    for lots in ParkingLot.query.all():
        available_count = lots.parking_spots.filter_by(status=False).count()
        occupied_count = lots.parking_spots.filter_by(status=True).count()

        lst_of_parking_lots_name.append(lots.prime_location_name)
        lst_of_parking_lots_available_count.append(available_count)
        lst_of_parking_lots_occupied_count.append(occupied_count)

    bar_width = 0.35
    available_row = np.arange(len(lst_of_parking_lots_name))
    occupied_row = [x + bar_width for x in available_row]

    plt.bar(available_row, lst_of_parking_lots_available_count, color='blue', width=bar_width, label='Available Parking Spots')
    plt.bar(occupied_row, lst_of_parking_lots_occupied_count, color='red', width=bar_width, label='Occupied Parking Spots')

    plt.xlabel('Parking Lot Name')
    plt.ylabel('Number of Available Spots')
    plt.title('Parking Lot Name / Number of Available  & Occupied Parking Spots')
    plt.xticks([r + bar_width / 2 for r in available_row], lst_of_parking_lots_name)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_relative_path = '..'
    project_root = os.path.join(script_dir, project_root_relative_path)
    project_root = os.path.abspath(project_root)
    output_folder_relative_to_root = 'static'
    output_folder = os.path.join(project_root, output_folder_relative_to_root)
    file_name = 'ParkingLot_slots.png'
    full_path = os.path.join(output_folder, file_name)

    plt.savefig(full_path, transparent=True)
    plt.close()

def revenue_chart():
    lst_of_parking_lots_name = []
    total_revenue_per_lot = []

    revenue_by_lot_name = {}

    completed_reservations = ReservedParkingSpot.query.filter(
        ReservedParkingSpot.is_active == False,
        ReservedParkingSpot.total_cost.isnot(None)
    ).all()

    for reservations in completed_reservations:
        if reservations.parking_spot != None:
            parking_lot_name = reservations.parking_spot.parking_lot.prime_location_name
        else:
            parking_lot_name = "Previous Parking Spots"
        current_revenue = reservations.total_cost

        revenue_by_lot_name[parking_lot_name] = revenue_by_lot_name.get(parking_lot_name, 0.0) + current_revenue

    for lot_name, revenue in revenue_by_lot_name.items():
        lst_of_parking_lots_name.append(lot_name)
        total_revenue_per_lot.append(int(revenue))

    plt.bar(lst_of_parking_lots_name, total_revenue_per_lot)
    plt.xlabel('Parking Lot Name')
    plt.ylabel('Total Revenue per Lot')
    plt.title('Parking Lot Name / Total Revenue per Lot')

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_relative_path = '..'
    project_root = os.path.join(script_dir, project_root_relative_path)
    project_root = os.path.abspath(project_root)
    output_folder_relative_to_root = 'static'
    output_folder = os.path.join(project_root, output_folder_relative_to_root)
    file_name = 'Total_Revenue_per_lot.png'
    full_path = os.path.join(output_folder, file_name)

    plt.savefig(full_path, transparent=True)
    plt.close()

def user_revenue_chart(user_id):
    lst_of_parking_lots_name = []
    total_revenue_per_lot = []

    revenue_by_lot_name = {}

    completed_reservations = ReservedParkingSpot.query.filter(
        ReservedParkingSpot.user_id == user_id,
        ReservedParkingSpot.is_active == False,
        ReservedParkingSpot.total_cost.isnot(None)
    ).all()

    for reservations in completed_reservations:
        if reservations.parking_spot != None:
            parking_lot_name = reservations.parking_spot.parking_lot.prime_location_name
        else:
            parking_lot_name = "Previous Parking Spots"
        current_revenue = reservations.total_cost

        revenue_by_lot_name[parking_lot_name] = revenue_by_lot_name.get(parking_lot_name, 0.0) + current_revenue

    for lot_name, revenue in revenue_by_lot_name.items():
        lst_of_parking_lots_name.append(lot_name)
        total_revenue_per_lot.append(int(revenue))

    plt.bar(lst_of_parking_lots_name, total_revenue_per_lot)
    plt.xlabel('Parking Lot Name')
    plt.ylabel('Total Expenditure per Lot')
    plt.title('Parking Lot Name / Total Expenditure per Lot')

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_relative_path = '..'
    project_root = os.path.join(script_dir, project_root_relative_path)
    project_root = os.path.abspath(project_root)
    output_folder_relative_to_root = 'static'
    output_folder = os.path.join(project_root, output_folder_relative_to_root)
    file_name = 'Total_Expenditure_per_user_lot.png'
    full_path = os.path.join(output_folder, file_name)

    plt.savefig(full_path, transparent=True)
    plt.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('home'))

        user = User.query.filter_by(username=username).first()

        if user:
            if user.password == password:
                session['user_id'] = user.id
                session['username'] = user.username
                session['full_name'] = user.full_name
                session['email'] = user.email
                session['phone_number'] = user.phone_number
                session['address'] = user.address

                if user.username == 'admin':
                    flash(f'Welcome,{user.full_name}!', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash(f'Welcome, {user.full_name}!', 'success')
                    return redirect(url_for('user_dashboard'))
            else:
                flash('Invalid Password', 'danger')
                return redirect(url_for('home'))
        else:
            flash('Invalid username', 'danger')
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')

        existing_user_username = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()

        if existing_user_username:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        if existing_user_email:
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('register'))
        if confirm_password != password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))


        user = User(username=username, password=password, full_name=full_name, email=email,
                    phone_number=phone_number, address=address)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('home'))
    if session.get('username') != 'admin':
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('home'))

    parking_lots = ParkingLot.query.all()
    parking_spots = ParkingSpot.query.all()


    return render_template('admin_dashboard.html', parking_lots=parking_lots, parking_spots=parking_spots)

@app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    if 'user_id' not in session:
        flash('Please log in to view your dashboard.', 'danger')
        return redirect(url_for('home'))
    parking_lots = ParkingLot.query.all()
    reserved_parking_spots = ReservedParkingSpot.query.filter_by(user_id=session['user_id']).all()

    return render_template('user_dashboard.html',
                           parking_lots=parking_lots,
                           reserved_parking_spots=reserved_parking_spots,
                           datetime=datetime)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template('edit_profile.html')
    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')

        user = User.query.filter_by(username=session['username']).first()

        user.full_name = full_name
        user.email = email
        user.phone_number = phone_number
        user.address = address
        db.session.commit()

        session['full_name'] = user.full_name
        session['email'] = user.email
        session['phone_number'] = user.phone_number
        session['address'] = user.address

        flash('Profile updated successfully!', 'success')

        if session['username'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))

    return render_template('edit_profile.html')

@app.route('/parking_lot', methods=['GET', 'POST'])
def parking_lot():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('home'))
    if session.get('username') != 'admin':
        flash('Unauthorized access to add parking lot.', 'danger')
        return redirect(url_for('admin_dashboard'))


    if request.method == 'POST':
        prime_location_name = request.form['prime_location_name']
        price = request.form['price']
        address = request.form['address']
        pin_code = request.form['pin_code']
        maximum_number_of_spots = request.form['maximum_number_of_spots']
        description = request.form['description']

        existing_lot = ParkingLot.query.filter_by(prime_location_name=prime_location_name).first()
        if existing_lot:
            flash(f"A parking lot with the name '{prime_location_name}' already exists. Please choose a different name.", 'danger')
            return redirect(url_for('admin_dashboard'))

        parking_lot = ParkingLot(prime_location_name=prime_location_name,price=price,address=address,pin_code=pin_code,
                                 maximum_number_of_spots=maximum_number_of_spots,description=description)

        db.session.add(parking_lot)
        db.session.commit()

        for spots in range(int(maximum_number_of_spots)):
            parking_spot = ParkingSpot(parking_lot_id=parking_lot.id, status=False, vehicle_plate=None)
            db.session.add(parking_spot)
        db.session.commit()

        flash('Parking Lot added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return redirect(url_for('admin_dashboard'))

@app.route('/registered_users', methods=['GET', 'POST'])
def registered_users():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('home'))
    if session.get('username') != 'admin':
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('home'))

    users = User.query.all()
    return render_template("registered_users.html", users=users)

@app.route('/edit_parking_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_parking_lot(lot_id):
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('home'))
    if session.get('username') != 'admin':
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_lot':
            lot_to_update = ParkingLot.query.get(lot_id)
            old_max_spots = lot_to_update.maximum_number_of_spots

            if not lot_to_update:
                flash('Error: Parking Lot not found for update.', 'danger')
                return redirect(url_for('admin_dashboard'))

            price = request.form.get('price')
            address = request.form.get('address')
            pin_code = request.form.get('pin_code')
            maximum_number_of_spots = request.form.get('maximum_number_of_spots')
            description = request.form.get('description')


            lot_to_update.price = price
            lot_to_update.address = address
            lot_to_update.pin_code = pin_code
            lot_to_update.description = description if description else None

            db.session.commit()

            lot_to_update.maximum_number_of_spots = maximum_number_of_spots

            current_occupied_spots = int(lot_to_update.parking_spots.filter_by(status=True).count())
            current_total_spots = int(lot_to_update.parking_spots.count()) #old spots
            maximum_number_of_spots= int(maximum_number_of_spots)  #new spots

            if maximum_number_of_spots  < current_occupied_spots:
                flash(
                    f'Cannot reduce maximum spots to {maximum_number_of_spots}. There are {current_occupied_spots} spots currently occupied.',
                    'danger')

                lot_to_update.maximum_number_of_spots = old_max_spots
                return redirect(url_for('admin_dashboard'))

            if maximum_number_of_spots > current_total_spots:
                spots_to_add = maximum_number_of_spots - current_total_spots
                for spots in range(spots_to_add):
                    new_spot = ParkingSpot(parking_lot_id=lot_to_update.id, status=False)
                    db.session.add(new_spot)
                flash(f'Parking Lot updated successfully. Added {spots_to_add} new spots.', 'success')

            elif maximum_number_of_spots < current_total_spots:
                spots_to_remove = current_total_spots - maximum_number_of_spots


                available_spots = lot_to_update.parking_spots.filter_by(status=False).limit(spots_to_remove).all()
                for spot in available_spots:
                    db.session.delete(spot)
                flash(f'Parking Lot updated successfully. Removed {spots_to_remove} spots.', 'success')
            else:
                flash('Parking Lot updated successfully!', 'success')
                return redirect(url_for('admin_dashboard'))

        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_dashboard.html', lot=lot_id)

@app.route('/delete_parking_lot/<int:lot_id>', methods=['GET', 'POST'])
def delete_parking_lot(lot_id):
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('home'))
    if session.get('username') != 'admin':
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'delete_lot':
            lot_to_delete = ParkingLot.query.get(lot_id)
            current_occupied_spots = int(lot_to_delete.parking_spots.filter_by(status=True).count())


            if not lot_to_delete:
                flash('Error: Parking Lot not found for delete.', 'danger')
                return redirect(url_for('admin_dashboard'))
            if current_occupied_spots > 0:
                flash(
                    f'Cannot Delete the Lot. There are {current_occupied_spots} spots currently occupied.',
                    'danger')
                return redirect(url_for('admin_dashboard'))


            db.session.delete(lot_to_delete)
            db.session.commit()
            flash('Parking Lot Deleted successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

    return render_template('admin_dashboard.html', lot=lot_id)

@app.route('/view_occupied_spot/<int:spot_id>', methods=['GET', 'POST'])
def view_occupied_spot(spot_id):
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('home'))
    if session.get('username') != 'admin':
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'view_occupied_spot':
            pass
    return render_template('admin_dashboard.html', spot=spot_id)

@app.route('/book_spot/<int:lot_id>', methods=['GET', 'POST'])
def book_spot(lot_id):
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('home'))
    if session.get('username') == 'admin':
        flash('Unauthorized access. Please log in as User.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'book_slot':
            id = lot_id
            user_id = session.get('user_id')
            spot_id = request.form.get('parking_spot_id')
            price = request.form['price']
            vehicle_plate = request.form.get('vehicle_plate')

            parking_spot = ParkingSpot.query.get(spot_id)

            if parking_spot:
                parking_spot.status = True
                parking_spot.vehicle_plate = vehicle_plate

                reserve_parking_spot = ReservedParkingSpot(spot_id=spot_id, user_id=user_id,
                                                           parking_cost_per_unit_time=price,
                                                           vehicle_plate=vehicle_plate,
                                                           is_active=True,
                                                           in_time=datetime.utcnow())
                db.session.add(reserve_parking_spot)
                db.session.commit()

            flash('Reservation successful!', 'success')
            return redirect(url_for('user_dashboard'))

        return redirect(url_for('user_dashboard'))

    return render_template('user_dashboard.html')

@app.route('/release_book_spot/<int:spot_id>', methods=['GET', 'POST'])
def release_book_spot(spot_id):
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('home'))
    if session.get('username') == 'admin':
        flash('Unauthorized access. Please log in as User.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'release_book_spot':
            id = spot_id

            release_spot = ReservedParkingSpot.query.get(id)

            if release_spot:
                release_spot.parking_spot.status = False
                release_spot.parking_spot.vehicle_plate = None
                release_spot.is_active = False
                release_spot.out_time = datetime.utcnow()

                if release_spot.in_time and release_spot.out_time:
                    total_duration = release_spot.out_time - release_spot.in_time
                    total_hours = (total_duration.total_seconds() / 3600)
                    if total_hours < 1:  # Minimum charge for an hour
                        total_hours = 1
                        release_spot.total_cost = total_hours * release_spot.parking_cost_per_unit_time
                    else:
                        total_hours = math.ceil(total_hours)
                        release_spot.total_cost = total_hours * release_spot.parking_cost_per_unit_time


            db.session.commit()

            flash('Reservation Released successful!', 'success')
            return redirect(url_for('user_dashboard'))

        return redirect(url_for('user_dashboard'))

    return render_template('user_dashboard.html')

@app.route('/summary', methods=['GET', 'POST'])
def summary():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('home'))
    if session.get('username') != 'admin':
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('home'))

    generate_parking_spots_chart()
    revenue_chart()
    return render_template('summary.html')

@app.route('/user_summary', methods=['GET', 'POST'])
def user_summary():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('home'))
    else:
        user_id = session.get('user_id')
    if session.get('username') == 'admin':
        flash('Unauthorized access. Please log in as user.', 'danger')
        return redirect(url_for('home'))

    generate_parking_spots_chart()
    revenue_chart()
    user_revenue_chart(user_id)

    return render_template('user_summary.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('home'))
