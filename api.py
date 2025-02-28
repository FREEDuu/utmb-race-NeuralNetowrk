from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import datetime
import torch
from model.NeuralNetwork.NeuralNetworkModel import RaceTimeNN

app = FastAPI()

# Load model and scaler
model_regression = joblib.load("models-binary/race_time_model.joblib")
scaler_regression = joblib.load("models-binary/scaler.joblib")
scaler_nn = joblib.load("models-binary/nn/scaler.joblib")

model = RaceTimeNN(input_size=4, scaler = scaler_nn)  # Match input size (4 features)
model.load_state_dict(torch.load("models-binary/nn/race_time_nn.pth"))
model.eval()  # Set to evaluation mode

class PredictionRequest(BaseModel):
    distance: float
    elevation: float
    utmb_index: int

def float_seconds_to_hms(seconds_float):
    """Converts a float representing seconds to HH:MM:SS format."""
    try:
        seconds = int(round(seconds_float))  # Round and convert to integer
        td = datetime.timedelta(seconds=seconds)
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    except (TypeError, ValueError):
        return "Invalid input"

@app.post("/predict")
async def predict(request: PredictionRequest):
    # Calculate elevation per km
    elevation_per_km = request.elevation / request.distance
    
    # Create feature array
    features = np.array([
        request.distance,
        request.elevation,
        request.utmb_index,
        elevation_per_km
    ]).reshape(1, -1)
    
    # Scale features
    scaled_features_regression = scaler_regression.transform(features)
    scaled_features_nn = scaler_nn.transform(features)
    
    # Predict
    prediction_regression = model_regression.predict(scaled_features_regression)
    predict_time = float_seconds_to_hms(prediction_regression[0])
        
    with torch.no_grad():
        input_tensor = torch.tensor(scaled_features_nn, dtype=torch.float32)
        prediction_nn = model(input_tensor).item()

    print(prediction_nn, predict_time)
    prediction_nn = float_seconds_to_hms(prediction_nn)

    return {"predicted_time_min_regression": predict_time,
            "predicted_time_min_nn": prediction_nn}