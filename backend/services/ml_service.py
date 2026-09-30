import os
import joblib
import pandas as pd

# Define paths relative to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILURE_MODEL_PATH = os.path.join(BASE_DIR, "models", "failure_predictor.pkl")
SUPPLY_MODEL_PATH = os.path.join(BASE_DIR, "models", "supply_chain_predictor.pkl")

# Load models into memory on startup
try:
    failure_model = joblib.load(FAILURE_MODEL_PATH)
except Exception as e:
    failure_model = None
    print(f"Warning: Failure model not found at {FAILURE_MODEL_PATH}. ({e})")

try:
    supply_model = joblib.load(SUPPLY_MODEL_PATH)
except Exception as e:
    supply_model = None
    print(f"Warning: Supply chain model not found at {SUPPLY_MODEL_PATH}. ({e})")

def predict_machine_failure(vibration: float, bearing_temp: float, motor_current: float, pressure: float):
    if not failure_model:
        return {"error": "Failure model not loaded."}
    
    input_data = pd.DataFrame([{
        'vibration_mm_s': vibration,
        'bearing_temp_c': bearing_temp,
        'motor_current_a': motor_current,
        'pressure_bar': pressure
    }])
    
    prediction = int(failure_model.predict(input_data)[0])
    probability = float(failure_model.predict_proba(input_data)[0][1]) * 100
    
    return {
        "breakdown_predicted": bool(prediction == 1),
        "failure_probability_score": round(probability, 2)
    }

def predict_dynamic_lead_time(part_no: str, season: str, market_condition: str):
    if not supply_model:
        return {"estimated_lead_time_days": 14} # Fallback default
    
    input_data = pd.DataFrame([{
        'part_no': part_no,
        'season': season,
        'market_condition': market_condition
    }])
    
    predicted_days = float(supply_model.predict(input_data)[0])
    return {"estimated_lead_time_days": round(predicted_days, 1)}