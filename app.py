import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from flask import Flask, render_template, request
import threading
import webbrowser

# Load and prepare the data. calories are our dataframe name
calories = pd.read_csv("calories.csv")
print(calories.head())
calories_clean = calories.drop("User_ID", axis=1)
print(calories_clean.head())

# Encode Gender
calories_clean.replace({"Gender" : {'male' : 1, 'female' : 0}}, inplace=True)

# Features and target
X = calories_clean.drop("Calories", axis=1)
y = calories_clean["Calories"]
print(X.head())
print(y.head())

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
print(X.shape, y.shape, X_train.shape, y_train.shape, X_test.shape, y_test.shape)
model = LinearRegression()
model.fit(X_train, y_train)

data_pred = model.predict(X_test)
print(data_pred)
model_accuracy = r2_score(y_test, data_pred)
model_accuracy = round(model_accuracy * 100, 2)

# Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        gender = 1 if request.form["gender"] == "Male" else 0
        age = float(request.form["age"])
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        duration = float(request.form["duration"])
        heart_rate = float(request.form["heart_rate"])
        body_temp = float(request.form["body_temp"])

        input_data = np.array([[gender, age, height, weight, duration, heart_rate, body_temp]])
        prediction = model.predict(input_data)[0]
        prediction = round(prediction, 2)
        return render_template("index.html", prediction=prediction, accuracy=model_accuracy)

    except Exception as e:
        return f"❌ Error: {e}"

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=False)