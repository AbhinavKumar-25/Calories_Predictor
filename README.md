# 🏋️‍♂️ Calories Burned Predictor — ML + Flask + MySQL Web Application

This project is a machine learning–powered web application that predicts how many calories a person burns during exercise based on key physical and workout parameters.
It integrates an ML model built with Scikit-Learn, a secure Flask backend, and a MySQL database to deliver end-to-end functionality.

## 🚀 Features
## 🔢 Machine Learning
- Linear Regression model trained on fitness dataset
- Data preprocessing: cleaning, encoding, feature selection
- Achieved 95% model accuracy (R² score)
- Model exported using Joblib and loaded into Flask for real-time predictions

## 🌐 Web Application (Flask)
- User registration and login system
- Secure authentication using Flask-Login
- Password hashing with Flask-Bcrypt
- Session-based user tracking
- Real-time calorie prediction UI
- Responsive frontend using HTML, CSS, and Jinja2 templates

## 🗄️ Database (MySQL + Flask-SQLAlchemy)
- Stores user registration data
- Saves each prediction with exercise input details and timestamp
- Dashboard for users to view all past predictions
- Clean ORM-based implementation using SQLAlchemy
  
## 📊 Input Features
The user provides the following details to get a calorie prediction:
- Gender
- Age
- Height (cm)
- Weight (kg)
- Duration (minutes)
- Heart Rate (bpm)
- Body Temperature (°C)

## 🧠 Model Workflow
1. Load and preprocess dataset
2. Encode categorical variables
3. Drop irrelevant columns
4. Train-test split
5. Train Linear Regression model
6. Evaluate and save using Joblib
7. Integrate model into Flask backend

## 📂 Project Structure
Calories_Predictor/
│── app.py                     # Flask backend
│── model.pkl                  # Trained ML model
│── calories.csv               # Dataset
│── requirements.txt           # Dependencies
│── README.md                  # Documentation
│
├── database/
│   └── models.py              # SQLAlchemy models
│
├── static/
│   └── style.css              # Frontend styling
│
└── templates/
    ├── index.html             # Prediction page
    ├── login.html             # Login form
    ├── register.html          # Registration form
    └── dashboard.html         # User history page


## ▶️ How to Run the Project
## 1️⃣ Install dependencies
pip install -r requirements.txt

## 2️⃣ Configure your MySQL database
Create a database:
CREATE DATABASE calories_predictor;
Update your DB URI inside your Flask app:
SQLALCHEMY_DATABASE_URI = "mysql://username:password@localhost/calories_predictor"

## 3️⃣ Run the Flask app
python app.py

Visit in browser:
👉 http://127.0.0.1:5000/

## 📊 Example Prediction
Input:
Gender: Male
Age: 25
Height: 175 cm
Weight: 70 kg
Duration: 30 minutes
Heart Rate: 120 bpm
Body Temp: 39.5 °C

Output:
Predicted Calories Burned: 245.67 kcal
Model Accuracy: 96.85%

## 💻 Tech Stack
## Backend
- Python
- Flask
- Flask-Login
- Flask-Bcrypt
- Flask-SQLAlchemy

## Machine Learning
- Pandas
- NumPy
- Scikit-Learn
- Joblib

## Frontend
- HTML
- CSS
- Jinja Templates

## Database
- MySQL

## Development
- VS Code

## 📝 Author
A Abhinav Kumar
