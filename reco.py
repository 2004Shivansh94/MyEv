from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib

# Real-life EV scooter data
data = {
    'model': ['Ather 450X', 'Ola S1 Pro', 'Bajaj Chetak', 'TVS iQube', 'Simple One', 'Hero Electric Optima', 'Ampere Magnus Pro', 'Greaves Electric ADO', 'Benling Aura', 'Yamaha EC-05'],
    'price': [139000, 139999, 149000, 119000, 109000, 70000, 80000, 75000, 90000, 120000],  # Prices in INR
    'range': [85, 181, 95, 75, 300, 60, 80, 70, 90, 100],  # Range in km
    'battery_capacity': [2.9, 4.0, 3.8, 3.0, 4.8, 1.5, 2.2, 1.8, 2.5, 3.0],  # Battery capacity in kWh
    'top_speed': [80, 115, 70, 78, 105, 45, 55, 50, 60, 70]  # Top speed in km/h
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define features (X) and labels (y)
X = df[['price', 'range', 'battery_capacity', 'top_speed']]
y = df['model']

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the KNN model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_scaled, y)

# Save the model and scaler
joblib.dump(knn, 'ev_recommendation_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Model and scaler saved successfully.")
