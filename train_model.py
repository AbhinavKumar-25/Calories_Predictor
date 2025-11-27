# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import joblib

# Load and prepare data
calories = pd.read_csv("calories.csv")
calories_clean = calories.drop("User_ID", axis=1)

# Encode Gender
calories_clean.replace({"Gender": {'male': 1, 'female': 0}}, inplace=True)

# Features and target
X = calories_clean.drop("Calories", axis=1)
y = calories_clean["Calories"]

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = r2_score(y_test, y_pred)
accuracy = round(accuracy * 100, 2)

# Save model and accuracy
joblib.dump(model, "model.pkl")
with open("model_accuracy.txt", "w") as f:
    f.write(str(accuracy))

print(f"✅ Model trained successfully!")
print(f"📈 Accuracy: {accuracy}%")
print(f"💾 Model saved as model.pkl")
