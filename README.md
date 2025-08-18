# Calories Predictor Web App

This project is a **Flask-based web application** that predicts the number of calories burned during physical activity based on user inputs such as gender, age, height, weight, duration, heart rate, and body temperature.  
The backend uses a **Linear Regression model (Scikit-learn)** trained on the provided dataset (`calories.csv`).

## 🚀 Features
- Train a **Linear Regression model** on the dataset
- Input fields: Gender, Age, Height, Weight, Duration, Heart Rate, Body Temperature
- Predict calories burned instantly through the web app
- Shows **model accuracy (R² score)** on the interface
- Flask + HTML/CSS frontend for easy interaction

## 🛠️ Tech Stack  
- **Python** → Core programming language  
- **Flask** → Backend framework for web application  
- **Pandas** → Data manipulation and preprocessing  
- **NumPy** → Numerical computations  
- **Scikit-learn** → Machine learning model building  
- **Matplotlib & Seaborn** → Data visualization  
- **HTML, CSS** → Frontend UI for the web app  
- **PyCharm** → Development environment  

## 📂 Project Structure
calories_predictor/
│── app.py # Flask app entry point
│── calories.csv # Dataset
│── static/
│ └── style.css # Styling
│── templates/
│ └── index.html # Frontend UI
│── requirements.txt # Dependencies
│── README.md # Project documentation

▶️ Usage
Run the Flask app:
python app.py
The app will automatically open in your browser at 👉 http://127.0.0.1:5000/

📊 Example Prediction
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
