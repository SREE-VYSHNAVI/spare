import pandas as pd
import os
import json

# Load CSV data files
TELEMETRY_FILE = 'backend/data/telemetry.csv' if os.path.exists('backend/data/telemetry.csv') else '../1_telemetry_data.csv'
BOM_FILE = 'backend/data/bom.csv' if os.path.exists('backend/data/bom.csv') else '../2_bom_mapping.csv'
INVENTORY_FILE = 'backend/data/inventory.csv' if os.path.exists('backend/data/inventory.csv') else '../3_inventory_master.csv'
LOGS_FILE = 'backend/data/logs.csv' if os.path.exists('backend/data/logs.csv') else '../4_maintenance_logs.csv'

def load_inventory_data():
    """Load inventory master data"""
    try:
        df = pd.read_csv(INVENTORY_FILE)
        return df.to_dict('records')
    except:
        # Return mock data if files don't exist
        return [
            {'part_no': 'BFP-PRT-BRG-01', 'part_name': 'Pump Thrust Bearing', 'current_stock': 1, 'vendor_lead_time_days': 10, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 45000},
            {'part_no': 'ST-PRT-BRG-01', 'part_name': 'Turbine Journal Bearing', 'current_stock': 0, 'vendor_lead_time_days': 15, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 250000},
            {'part_no': 'CWP-PRT-IMP-03', 'part_name': 'Cooling Water Impeller', 'current_stock': 0, 'vendor_lead_time_days': 14, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 75000},
            {'part_no': 'CC-PRT-BLT-01', 'part_name': 'Steel-Cord Conveyor Belt', 'current_stock': 0, 'vendor_lead_time_days': 8, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 12500},
            {'part_no': 'GEN-PRT-FAN-02', 'part_name': 'Stator Cooling Fan Blade', 'current_stock': 2, 'vendor_lead_time_days': 8, 'operational_criticality': 'CRITICAL_MEDIUM', 'unit_cost_inr': 35000},
            {'part_no': 'BFP-PRT-SEAL-02', 'part_name': 'High-Pressure Mechanical Seal', 'current_stock': 0, 'vendor_lead_time_days': 6, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 12000},
        ]

def load_bom_data():
    """Load Bill of Materials data"""
    try:
        df = pd.read_csv(BOM_FILE)
        return df.to_dict('records')
    except:
        return []

def get_executive_summary() -> dict:
    """
    Generate executive summary dashboard metrics
    """
    inventory = load_inventory_data()
    
    total_parts = len(inventory)
    critical_stock_out = sum(1 for item in inventory if item['current_stock'] == 0)
    total_in_stock = sum(item.get('current_stock', 0) for item in inventory)
    avg_lead_time = sum(item.get('vendor_lead_time_days', 0) for item in inventory) / max(len(inventory), 1)
    
    return {
        "total_assets": 5,  # 5 thermal power plant assets
        "total_parts_managed": total_parts,
        "critical_alerts": critical_stock_out,
        "parts_in_stock": total_in_stock,
        "avg_lead_time": round(avg_lead_time, 1),
        "system_status": "Operational"
    }

def get_inventory_status() -> list:
    """
    Get current inventory status with all spare parts
    """
    return load_inventory_data()

def get_bom_mapping_details(asset_id: str) -> dict:
    """
    Get Bill of Materials mapping for a specific asset
    """
    bom = load_bom_data()
    asset_bom = [item for item in bom if item.get('asset_tag') == asset_id]
    
    return {
        "asset_id": asset_id,
        "bom_items": asset_bom,
        "total_parts": len(asset_bom)
    }
