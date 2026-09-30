import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

# Initialize models
failure_model = None
lead_time_model = None
scaler = None

def load_models():
    """Load or train ML models"""
    global failure_model, lead_time_model, scaler
    
    # For now, we'll use simple mock predictions
    # In production, these would be trained models
    pass

def predict_machine_failure(vibration: float, bearing_temp: float, motor_current: float, pressure: float) -> dict:
    """
    Predict machine failure based on sensor readings
    """
    # Thresholds based on dataa.py
    failure_score = 0.0
    
    # High vibration indicates failure
    if vibration > 6.0:
        failure_score += 0.4
    elif vibration > 4.0:
        failure_score += 0.2
    
    # High bearing temperature
    if bearing_temp > 90:
        failure_score += 0.3
    elif bearing_temp > 80:
        failure_score += 0.15
    
    # High motor current
    if motor_current > 200:
        failure_score += 0.2
    elif motor_current > 180:
        failure_score += 0.1
    
    # Low pressure
    if pressure < 70:
        failure_score += 0.1
    
    # Cap at 1.0
    failure_probability = min(failure_score, 1.0)
    
    # Recommend parts based on failure prediction
    recommended_parts = []
    if vibration > 5.0:
        recommended_parts.extend(['BFP-PRT-BRG-01', 'ST-PRT-BRG-01', 'CC-PRT-BRG-02'])
    if bearing_temp > 85:
        recommended_parts.extend(['GEN-PRT-FAN-02', 'CWP-PRT-SEAL-02'])
    if motor_current > 200:
        recommended_parts.extend(['BFP-PRT-CPL-05', 'CC-PRT-MTR-04'])
    if pressure < 70:
        recommended_parts.extend(['BFP-PRT-SEAL-02', 'CWP-PRT-IMP-03'])
    
    return {
        "failure_probability": round(failure_probability, 3),
        "risk_level": "CRITICAL" if failure_probability > 0.7 else "WARNING" if failure_probability > 0.4 else "NORMAL",
        "recommended_parts": list(set(recommended_parts)),
        "sensor_readings": {
            "vibration_mm_s": vibration,
            "bearing_temp_c": bearing_temp,
            "motor_current_a": motor_current,
            "pressure_bar": pressure
        }
    }

def predict_dynamic_lead_time(part_no: str, season: str, market_condition: str) -> dict:
    """
    Predict delivery lead time based on part, season, and market condition
    Based on demandofspare.py logic
    """
    # Base lead times from inventory_master
    base_lead_times = {
        'BFP-PRT-BRG-01': 10,
        'ST-PRT-BLD-02': 30,
        'CWP-PRT-IMP-03': 14,
        'CC-PRT-BLT-01': 8,
        'BFP-PRT-SEAL-02': 6,
        'ST-PRT-BRG-01': 15,
        'GEN-PRT-EXC-03': 18,
        'CC-PRT-GBX-05': 20,
    }
    
    base_time = base_lead_times.get(part_no, 14)
    predicted_time = base_time
    
    # Monsoon adds 3-8 days
    if season == 'Monsoon':
        predicted_time += np.random.randint(3, 8)
    
    # High demand adds 5-15 days
    if 'High Demand' in market_condition or 'Shortage' in market_condition:
        predicted_time += np.random.randint(5, 15)
    
    # Random variance
    predicted_time += np.random.randint(-2, 3)
    predicted_time = max(1, predicted_time)
    
    return {
        "part_no": part_no,
        "predicted_lead_time": int(predicted_time),
        "season": season,
        "market_condition": market_condition,
        "base_lead_time": base_time,
        "notes": f"Estimated delivery in {predicted_time} days considering {season} season and {market_condition} market conditions."
    }
