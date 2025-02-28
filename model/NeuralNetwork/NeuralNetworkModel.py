import torch
import torch.nn as nn
import torch.optim as optim
from model.process import process_data
import joblib
from sklearn.metrics import mean_absolute_error, r2_score

class RaceTimeNN(nn.Module):
    def __init__(self, input_size, scaler):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, 64),    # Input layer
            nn.ReLU(),                     # Non-linear activation
            nn.Linear(64, 32),             # Hidden layer
            nn.ReLU(),
            nn.Linear(32, 1)               # Output layer (predicted time)
        )
        self.scaler = scaler    
    
    def forward(self, x):
        return self.layers(x)
    
    def save(self):

        torch.save(model.state_dict(), "models-binary/nn/race_time_nn.pth")
        joblib.dump(self.scaler, "models-binary/nn/scaler.joblib")

    def train_nn(self, epochs=200):

        for epoch in range(epochs):
            # Forward pass
            outputs = model(X_train_tensor)
            loss = criterion(outputs, y_train_tensor)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if (epoch+1) % 20 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

if __name__ == "__main__":

    X_train_scaled, X_test_scaled, y_train, y_test, scaler = process_data()
    X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32).reshape(-1, 1)
    X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)

    model = RaceTimeNN(X_train_scaled.shape[1], scaler)

    # Loss and optimizer
    criterion = nn.MSELoss()  # Mean Squared Error (regression)
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    model.train_nn()


    with torch.no_grad():
        y_pred_tensor = model(X_test_tensor)
    y_pred = y_pred_tensor.numpy().flatten()

    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"MAE: {mae:.2f} minutes, R²: {r2:.2f}")

    model.save()