import joblib
from model.RegressionModel.train import get_model

model, scaler = get_model()
joblib.dump(model, "models-binary/race_time_model.joblib")
joblib.dump(scaler, "models-binary/scaler.joblib")