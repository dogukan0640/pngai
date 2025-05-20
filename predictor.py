import torch
import pandas as pd
import joblib
from lstm_model import LSTM

def make_prediction(symbol="BTCUSDT"):
    try:
        df = pd.read_csv("data/market_data.csv")
        df = df[df["symbol"] == symbol].tail(20)

        scaler = joblib.load("models/scaler.pkl")
        model = LSTM(input_size=3, hidden_size=64, num_layers=2)
        model.load_state_dict(torch.load("models/lstm_model.pth", map_location="cpu"))
        model.eval()

        data_scaled = scaler.transform(df[["price", "funding_rate", "open_interest"]].values)
        sequence = torch.tensor([data_scaled[-10:]], dtype=torch.float32)
        prediction = model(sequence).item()
        return f"{symbol} ➜ {prediction:.4f}"
    except Exception as e:
        return f"HATA (predictor): {e}"
