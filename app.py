# app.py
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
import numpy as np
import joblib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/calories_predictor'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# ------------------ MODELS ------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(16), nullable=False)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.relationship('UserProgress', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    duration = db.Column(db.Float)
    heart_rate = db.Column(db.Float)
    body_temp = db.Column(db.Float)
    predicted_calories = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ------------------ LOAD MODEL ------------------
model = joblib.load("model.pkl")
with open("model_accuracy.txt", "r") as f:
    model_accuracy = f.read().strip()


# ------------------ ROUTES ------------------
@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('predict'))  # or dashboard

    if request.method == 'POST':
        identifier = request.form['identifier']  # can be email or username
        password = request.form['password']

        # Try finding user by email OR username
        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()

        if user and user.check_password(password):
            login_user(user)
            flash('✅ Login successful!', 'success')
            return redirect(url_for('predict'))
        else:
            flash('❌ Invalid username/email or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash('👋 Logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Clear any leftover flash messages (like "Login successful!")
    session.pop('_flashes', None)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if email or username already exists
        if User.query.filter_by(email=email).first():
            flash('⚠️ Email already exists. Please use another or login instead.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('⚠️ Username already taken. Please choose another.', 'danger')
            return redirect(url_for('register'))

        # Check password confirmation
        if password != confirm_password:
            flash('❌ Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('register'))

        # Create user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # ✅ Instead of logging them in immediately:
        flash('🎉 Account created successfully! Please login to continue.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    if request.method == "POST":
        try:
            gender = current_user.gender
            if not gender:
                gender = request.form["gender"]
                current_user.gender = gender
                db.session.commit()

            # Collect inputs
            age = float(request.form["age"])
            height = float(request.form["height"])
            weight = float(request.form["weight"])
            duration = float(request.form["duration"])
            heart_rate = float(request.form["heart_rate"])
            body_temp = float(request.form["body_temp"])

            # Predict
            input_data = np.array([[1 if gender.lower() == "male" else 0,
                                    age, height, weight, duration, heart_rate, body_temp]])
            prediction = round(model.predict(input_data)[0], 2)

            # Save progress
            new_entry = UserProgress(
                user_id=current_user.id,
                gender=gender,
                age=age,
                height=height,
                weight=weight,
                duration=duration,
                heart_rate=heart_rate,
                body_temp=body_temp,
                predicted_calories=prediction
            )
            db.session.add(new_entry)
            db.session.commit()

            user_data = UserProgress.query.filter_by(user_id=current_user.id).order_by(
                UserProgress.timestamp.desc()).all()

            return render_template("predict.html", prediction=prediction,
                                   accuracy=model_accuracy, progress=user_data,
                                   user=current_user)

        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    user_data = UserProgress.query.filter_by(user_id=current_user.id).order_by(
        UserProgress.timestamp.desc()).all()
    return render_template("predict.html", progress=user_data, user=current_user)


# ------------------ AUTO OPEN ------------------
import threading, webbrowser
from werkzeug.serving import is_running_from_reloader

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    if not is_running_from_reloader():
        threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
