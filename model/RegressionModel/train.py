from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from process import process_data

def get_model():

    X_train_scaled, X_test_scaled, y_train, y_test, scaler = process_data()

    model = XGBRegressor(n_estimators=200, max_depth=5)
    model.fit(X_train_scaled, y_train)

    # Evaluate
    y_pred = model.predict(X_test_scaled)
    print(f"MAE: {mean_absolute_error(y_test, y_pred)/60:.2f} minutes")
    return model, scaler