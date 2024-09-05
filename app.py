# app.py
from flask import Flask, request, render_template
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)

# Load model and scaler
model = joblib.load('ev_recommendation_model.pkl')
scaler = joblib.load('scaler.pkl')  # Ensure you have this file or remove this line if not used

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    price = float(request.form['price'])
    ev_range = float(request.form['range'])
    battery_capacity = float(request.form['battery_capacity'])
    top_speed = float(request.form['top_speed'])

    # Scale input data
    customer_input = [[price, ev_range, battery_capacity, top_speed]]
    customer_input_scaled = scaler.transform(customer_input)

    # Predict using the model
    prediction = model.predict(customer_input_scaled)
    return render_template('index.html', prediction=prediction[0])

if __name__ == "__main__":
    app.run(debug=True)
