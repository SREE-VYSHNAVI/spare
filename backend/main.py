from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.ml_service import predict_machine_failure, predict_dynamic_lead_time
from services.inventory_service import get_executive_summary, get_inventory_status, get_bom_mapping_details
from services.ai_service import ask_sparewise_assistant

app = FastAPI(
    title="SpareWise AI Backend",
    description="API for Thermal Power Plant Spare Parts Demand & Maintenance Prioritization",
    version="1.0.0"
)

# Enable CORS for React frontend (Vite default port 5173 or 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Request Schemas ---
class SensorInput(BaseModel):
    vibration_mm_s: float
    bearing_temp_c: float
    motor_current_a: float
    pressure_bar: float

class LeadTimeInput(BaseModel):
    part_no: str
    season: str
    market_condition: str

class ChatQuery(BaseModel):
    query: str

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"status": "online", "system": "SpareWise AI Engine Active"}

@app.get("/api/dashboard")
def api_dashboard_summary():
    return get_executive_summary()

@app.get("/api/inventory")
def api_inventory_list():
    return get_inventory_status()

@app.get("/api/bom-mapping/{asset_id}")
def api_bom_mapping(asset_id: str):
    return get_bom_mapping_details(asset_id)

@app.post("/api/predict/failure")
def api_predict_failure(sensors: SensorInput):
    result = predict_machine_failure(
        sensors.vibration_mm_s,
        sensors.bearing_temp_c,
        sensors.motor_current_a,
        sensors.pressure_bar
    )
    return result

@app.post("/api/predict/lead-time")
def api_predict_lead_time(data: LeadTimeInput):
    result = predict_dynamic_lead_time(
        data.part_no,
        data.season,
        data.market_condition
    )
    return result

@app.post("/api/ai/query")
def api_ai_query(chat: ChatQuery):
    summary = get_executive_summary()
    inventory = get_inventory_status()
    context = {"summary": summary, "inventory": inventory}
    
    answer = ask_sparewise_assistant(chat.query, context)
    return {"response": answer}