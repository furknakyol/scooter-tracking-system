from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Scooter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), nullable=False)
    battery_level = db.Column(db.Integer)
    status = db.Column(db.String(30))
    location = db.Column(db.String(100))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scooters', methods=['GET', 'POST'])
def scooters():
    if request.method == 'POST':
        model = request.form['model']
        battery_level = request.form['battery_level']
        status = request.form['status']
        location = request.form['location']
        new_scooter = Scooter(model=model, battery_level=battery_level, status=status, location=location)
        db.session.add(new_scooter)
        db.session.commit()
        return redirect(url_for('scooters'))
    all_scooters = Scooter.query.all()
    return render_template('scooters.html', scooters=all_scooters)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        new_user = User(name=name, email=email, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users'))
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scooter_id = db.Column(db.Integer, db.ForeignKey('scooter.id'), nullable=False)
    start_time = db.Column(db.String(50))
    end_time = db.Column(db.String(50))
    distance = db.Column(db.Float)
    cost = db.Column(db.Float)

@app.route('/rides', methods=['GET', 'POST'])
def rides():
    users = User.query.all()
    scooters = Scooter.query.all()
    if request.method == 'POST':
        user_id = request.form['user_id']
        scooter_id = request.form['scooter_id']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        distance = request.form['distance']
        cost = request.form['cost']
        new_ride = Ride(
            user_id=user_id,
            scooter_id=scooter_id,
            start_time=start_time,
            end_time=end_time,
            distance=distance,
            cost=cost
        )
        db.session.add(new_ride)
        db.session.commit()
        return redirect(url_for('rides'))
    all_rides = Ride.query.all()
    return render_template('rides.html', rides=all_rides, users=users, scooters=scooters)

class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scooter_id = db.Column(db.Integer, db.ForeignKey('scooter.id'), nullable=False)
    date = db.Column(db.String(50))
    description = db.Column(db.String(200))
    status = db.Column(db.String(30))

@app.route('/maintenances', methods=['GET', 'POST'])
def maintenances():
    scooters = Scooter.query.all()
    if request.method == 'POST':
        scooter_id = request.form['scooter_id']
        date = request.form['date']
        description = request.form['description']
        status = request.form['status']
        new_maintenance = Maintenance(
            scooter_id=scooter_id,
            date=date,
            description=description,
            status=status
        )
        db.session.add(new_maintenance)
        db.session.commit()
        return redirect(url_for('maintenances'))
    all_maintenances = Maintenance.query.all()
    return render_template('maintenances.html', maintenances=all_maintenances, scooters=scooters)

with app.app_context():
    db.create_all()
    
    
if __name__ == '__main__':
    app.run(debug=True)
