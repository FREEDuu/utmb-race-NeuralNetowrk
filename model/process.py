from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd 

def process_data():

    finalDF = pd.read_csv("/home/francesco/Desktop/PersonalProject/utmb-race-NeuralNetowrk/database/data/final_cleaned.csv")

    # Define features and target
    X = finalDF[["race_distance", "race_elevation", "runner_utmb_index", "elevation_per_km"]]
    y = finalDF["finish_hours"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler