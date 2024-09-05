from flask import Flask, request, render_template
import joblib

app = Flask(__name__)

# Load the saved AI model and scaler
model = joblib.load('ev_recommendation_model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get user inputs from the form
    price = float(request.form['price'])
    ev_range = float(request.form['range'])
    battery_capacity = float(request.form['battery_capacity'])
    top_speed = float(request.form['top_speed'])

    # Print inputs for debugging
    print(f"Received input: price={price}, range={ev_range}, battery_capacity={battery_capacity}, top_speed={top_speed}")

    # Predict using the model
    customer_input = [[price, ev_range, battery_capacity, top_speed]]
    customer_input_scaled = scaler.transform(customer_input)
    prediction = model.predict(customer_input_scaled)

    # Print prediction for debugging
    print(f"Prediction: {prediction[0]}")

    return render_template('index.html', prediction=prediction[0])

if __name__ == "__main__":
    app.run(debug=True)
