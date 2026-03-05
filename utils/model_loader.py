# utils/model_loader.py
import joblib

# ============================
# Load best models 
# ============================


harvest_model = joblib.load("models/harvest_gb.pkl")  


price_model = joblib.load("models/price_ridge.pkl")  

# ============================
# Load scalers
# ============================

harvest_scaler = joblib.load("models/harvest_scaler.pkl")
price_scaler   = joblib.load("models/price_scaler.pkl")

# ============================
# Feature lists 
# ============================

harvest_features = [
    'Month_num', 'Temperature_C', 'Rainfall_mm',
    'Prev_Harvest_kg', 'Fertilizer_kg',
    'Demand_Index', 'Supply_Index', 'Holiday'
]

price_features = harvest_features + [
    'Prev_price', 'Price_Lag1', 'Price_Lag2',
    'Price_MA3', 'Price_MA6',
    'Month_only', 'Quarter'
]