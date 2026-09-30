import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducible synthetic data
np.random.seed(42)

# ==========================================
# 1. TIME-SERIES TELEMETRY DATA (Table 1)
# Generating 30 days of hourly sensor readings across 5 thermal power plant assets.
# ==========================================
days = 30
timestamps = pd.date_range(end=datetime.today(), periods=days*24, freq='h')
num_records = len(timestamps)

assets = [
    'BFP-01',   # Boiler Feedwater Pump
    'ST-01',    # Steam Turbine
    'GEN-01',   # Generator
    'CWP-01',   # Cooling Water Pump
    'CC-01'     # Coal Conveyor
]

telemetry_list = []

for asset in assets:
    # Baseline normal sensor signals
    vibration = np.random.normal(loc=2.0, scale=0.3, size=num_records)
    bearing_temp = np.random.normal(loc=65.0, scale=3.0, size=num_records)
    motor_current = np.random.normal(loc=150.0, scale=10.0, size=num_records)
    pressure = np.random.normal(loc=100.0, scale=5.0, size=num_records)
    breakdown_flag = np.zeros(num_records, dtype=int)
    
    # Inject synthetic failure patterns for specific assets in the last few days
    if asset == 'BFP-01': # Cavitation & Mechanical Seal failure
        pressure[-72:] = np.random.normal(loc=65.0, scale=8.0, size=72)
        vibration[-72:] = np.random.normal(loc=6.5, scale=0.8, size=72)
        breakdown_flag[-72:] = 1
    elif asset == 'ST-01': # Rotor Imbalance & Bearing Wear
        vibration[-120:] = np.random.normal(loc=9.0, scale=1.1, size=120)
        bearing_temp[-120:] = np.random.normal(loc=95.0, scale=4.0, size=120)
        breakdown_flag[-120:] = 1
    elif asset == 'CC-01': # Belt wear & Motor overload
        motor_current[-48:] = np.random.normal(loc=220.0, scale=15.0, size=48)
        breakdown_flag[-48:] = 1

    df_asset = pd.DataFrame({
        'timestamp': timestamps,
        'asset_tag': asset,
        'vibration_mm_s': np.round(vibration, 2),
        'bearing_temp_c': np.round(bearing_temp, 1),
        'motor_current_a': np.round(motor_current, 1),
        'pressure_bar': np.round(pressure, 1),
        'breakdown_flag': breakdown_flag
    })
    telemetry_list.append(df_asset)

telemetry_df = pd.concat(telemetry_list, ignore_index=True)

# ==========================================
# 2. BILL OF MATERIALS (BOM) MAPPING (Table 2)
# Links failure modes and signals directly to exact spare parts for all 5 machines.
# ==========================================
bom_df = pd.DataFrame([
    # Boiler Feedwater Pump
    {'asset_tag': 'BFP-01', 'failure_mode': 'Bearing failure', 'signal_trigger': 'High vibration', 'part_no': 'BFP-PRT-BRG-01', 'sub_assembly': 'Pump Shaft Assembly'},
    {'asset_tag': 'BFP-01', 'failure_mode': 'Seal leakage', 'signal_trigger': 'Pressure drop', 'part_no': 'BFP-PRT-SEAL-02', 'sub_assembly': 'Mechanical Seal Housing'},
    {'asset_tag': 'BFP-01', 'failure_mode': 'Impeller damage', 'signal_trigger': 'Low flow rate', 'part_no': 'BFP-PRT-IMP-03', 'sub_assembly': 'Internal Impeller Unit'},
    {'asset_tag': 'BFP-01', 'failure_mode': 'Cavitation', 'signal_trigger': 'Pressure drop & vibration', 'part_no': 'BFP-PRT-GSK-04', 'sub_assembly': 'Suction Gasket/Valve'},
    {'asset_tag': 'BFP-01', 'failure_mode': 'Motor overload', 'signal_trigger': 'Motor current spike', 'part_no': 'BFP-PRT-CPL-05', 'sub_assembly': 'Motor Drive Coupling'},

    # Steam Turbine
    {'asset_tag': 'ST-01', 'failure_mode': 'Bearing wear', 'signal_trigger': 'High vibration & bearing temp', 'part_no': 'ST-PRT-BRG-01', 'sub_assembly': 'Rotor Support Bearing'},
    {'asset_tag': 'ST-01', 'failure_mode': 'Blade damage', 'signal_trigger': 'Rotor imbalance vibration', 'part_no': 'ST-PRT-BLD-02', 'sub_assembly': 'Turbine Rotor Blades'},
    {'asset_tag': 'ST-01', 'failure_mode': 'Valve failure', 'signal_trigger': 'Steam pressure instability', 'part_no': 'ST-PRT-VLV-03', 'sub_assembly': 'Main Steam Throttle Valve'},
    {'asset_tag': 'ST-01', 'failure_mode': 'Overheating', 'signal_trigger': 'High steam temperature', 'part_no': 'ST-PRT-GSK-04', 'sub_assembly': 'Casing Gaskets'},
    {'asset_tag': 'ST-01', 'failure_mode': 'Rotor imbalance', 'signal_trigger': 'High vibration frequency', 'part_no': 'ST-PRT-CPL-05', 'sub_assembly': 'Turbine Coupling'},

    # Generator
    {'asset_tag': 'GEN-01', 'failure_mode': 'Bearing failure', 'signal_trigger': 'Bearing temperature spike', 'part_no': 'GEN-PRT-BRG-01', 'sub_assembly': 'Main Bearing Block'},
    {'asset_tag': 'GEN-01', 'failure_mode': 'Cooling failure', 'signal_trigger': 'High winding temperature', 'part_no': 'GEN-PRT-FAN-02', 'sub_assembly': 'Stator Cooling Fan'},
    {'asset_tag': 'GEN-01', 'failure_mode': 'Excitation failure', 'signal_trigger': 'Voltage fluctuation', 'part_no': 'GEN-PRT-EXC-03', 'sub_assembly': 'Exciter Module'},
    {'asset_tag': 'GEN-01', 'failure_mode': 'Insulation failure', 'signal_trigger': 'Current leak', 'part_no': 'GEN-PRT-SEL-04', 'sub_assembly': 'Generator Seal Ring'},
    {'asset_tag': 'GEN-01', 'failure_mode': 'Overheating', 'signal_trigger': 'High winding temp', 'part_no': 'GEN-PRT-CBK-05', 'sub_assembly': 'Circuit Breaker Unit'},

    # Cooling Water Pump
    {'asset_tag': 'CWP-01', 'failure_mode': 'Bearing wear', 'signal_trigger': 'Vibration & bearing temp', 'part_no': 'CWP-PRT-BRG-01', 'sub_assembly': 'Pump Journal Bearing'},
    {'asset_tag': 'CWP-01', 'failure_mode': 'Seal leakage', 'signal_trigger': 'Pressure drop', 'part_no': 'CWP-PRT-SEAL-02', 'sub_assembly': 'Mechanical Seal'},
    {'asset_tag': 'CWP-01', 'failure_mode': 'Impeller damage', 'signal_trigger': 'Flow rate drop', 'part_no': 'CWP-PRT-IMP-03', 'sub_assembly': 'Bronze Impeller'},
    {'asset_tag': 'CWP-01', 'failure_mode': 'Motor failure', 'signal_trigger': 'Motor current spike', 'part_no': 'CWP-PRT-SFT-04', 'sub_assembly': 'Drive Shaft'},
    {'asset_tag': 'CWP-01', 'failure_mode': 'Cavitation', 'signal_trigger': 'Fluctuating pressure', 'part_no': 'CWP-PRT-CPL-05', 'sub_assembly': 'Shaft Coupling'},

    # Coal Conveyor
    {'asset_tag': 'CC-01', 'failure_mode': 'Belt wear/breakage', 'signal_trigger': 'Belt tension drop', 'part_no': 'CC-PRT-BLT-01', 'sub_assembly': 'Heavy Rubber Conveyor Belt'},
    {'asset_tag': 'CC-01', 'failure_mode': 'Bearing failure', 'signal_trigger': 'Vibration spike', 'part_no': 'CC-PRT-BRG-02', 'sub_assembly': 'Pulley Bearing'},
    {'asset_tag': 'CC-01', 'failure_mode': 'Roller failure', 'signal_trigger': 'Belt speed drop', 'part_no': 'CC-PRT-RLR-03', 'sub_assembly': 'Impact Roller Array'},
    {'asset_tag': 'CC-01', 'failure_mode': 'Motor overload', 'signal_trigger': 'High motor current', 'part_no': 'CC-PRT-MTR-04', 'sub_assembly': '3-Phase Drive Motor'},
    {'asset_tag': 'CC-01', 'failure_mode': 'Gearbox failure', 'signal_trigger': 'Vibration & temp spike', 'part_no': 'CC-PRT-GBX-05', 'sub_assembly': 'Reduction Gearbox'}
])

# ==========================================
# 3. INVENTORY & SUPPLY CHAIN MASTER (Table 3)
# Tracks spare part availability, vendor lead times, and operational criticality.
# ==========================================
inventory_df = pd.DataFrame([
    {'part_no': 'BFP-PRT-BRG-01', 'part_name': 'Pump Thrust Bearing', 'current_stock': 1, 'vendor_lead_time_days': 10, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 45000},
    {'part_no': 'BFP-PRT-SEAL-02', 'part_name': 'High-Pressure Mechanical Seal', 'current_stock': 0, 'vendor_lead_time_days': 6, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 12000},
    {'part_no': 'BFP-PRT-IMP-03', 'part_name': 'Stainless Steel Impeller', 'current_stock': 1, 'vendor_lead_time_days': 20, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 180000},
    {'part_no': 'BFP-PRT-GSK-04', 'part_name': 'High-Temp Flange Gasket', 'current_stock': 5, 'vendor_lead_time_days': 3, 'operational_criticality': 'CRITICAL_MEDIUM', 'unit_cost_inr': 2500},
    {'part_no': 'BFP-PRT-CPL-05', 'part_name': 'Flexible Motor Coupling', 'current_stock': 2, 'vendor_lead_time_days': 7, 'operational_criticality': 'CRITICAL_MEDIUM', 'unit_cost_inr': 15000},

    {'part_no': 'ST-PRT-BRG-01', 'part_name': 'Turbine Journal Bearing', 'current_stock': 0, 'vendor_lead_time_days': 15, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 250000},
    {'part_no': 'ST-PRT-BLD-02', 'part_name': 'Rotor Blade Segment', 'current_stock': 1, 'vendor_lead_time_days': 30, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 500000},
    {'part_no': 'ST-PRT-VLV-03', 'part_name': 'Steam Throttle Valve Actuator', 'current_stock': 1, 'vendor_lead_time_days': 12, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 95000},
    {'part_no': 'ST-PRT-GSK-04', 'part_name': 'High-Pressure Steam Gasket Set', 'current_stock': 3, 'vendor_lead_time_days': 4, 'operational_criticality': 'CRITICAL_MEDIUM', 'unit_cost_inr': 8000},
    {'part_no': 'ST-PRT-CPL-05', 'part_name': 'Turbine Gear Coupling', 'current_stock': 2, 'vendor_lead_time_days': 10, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 110000},

    {'part_no': 'GEN-PRT-BRG-01', 'part_name': 'Generator Sleeve Bearing', 'current_stock': 1, 'vendor_lead_time_days': 14, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 180000},
    {'part_no': 'GEN-PRT-FAN-02', 'part_name': 'Stator Cooling Fan Blade', 'current_stock': 2, 'vendor_lead_time_days': 8, 'operational_criticality': 'CRITICAL_MEDIUM', 'unit_cost_inr': 35000},
    {'part_no': 'GEN-PRT-EXC-03', 'part_name': 'Brushless Exciter Component', 'current_stock': 0, 'vendor_lead_time_days': 18, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 140000},
    {'part_no': 'GEN-PRT-SEL-04', 'part_name': 'Hydrogen Seal Ring', 'current_stock': 2, 'vendor_lead_time_days': 9, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 28000},
    {'part_no': 'GEN-PRT-CBK-05', 'part_name': 'Vacuum Circuit Breaker Unit', 'current_stock': 1, 'vendor_lead_time_days': 21, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 320000},

    {'part_no': 'CWP-PRT-BRG-01', 'part_name': 'Pump Roller Bearing', 'current_stock': 2, 'vendor_lead_time_days': 7, 'operational_criticality': 'CRITICAL_MEDIUM', 'unit_cost_inr': 22000},
    {'part_no': 'CWP-PRT-SEAL-02', 'part_name': 'Water Pump Mechanical Seal', 'current_stock': 1, 'vendor_lead_time_days': 5, 'operational_criticality': 'CRITICAL_MEDIUM', 'unit_cost_inr': 9500},
    {'part_no': 'CWP-PRT-IMP-03', 'part_name': 'Cooling Water Impeller', 'current_stock': 0, 'vendor_lead_time_days': 14, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 75000},
    {'part_no': 'CWP-PRT-SFT-04', 'part_name': 'Stainless Drive Shaft', 'current_stock': 1, 'vendor_lead_time_days': 12, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 60000},
    {'part_no': 'CWP-PRT-CPL-05', 'part_name': 'Pump Rubber Coupling', 'current_stock': 4, 'vendor_lead_time_days': 3, 'operational_criticality': 'CRITICAL_MEDIUM', 'unit_cost_inr': 4500},

    {'part_no': 'CC-PRT-BLT-01', 'part_name': 'Steel-Cord Conveyor Belt (100m)', 'current_stock': 0, 'vendor_lead_time_days': 8, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 125000},
    {'part_no': 'CC-PRT-BRG-02', 'part_name': 'Pulley Pillow Block Bearing', 'current_stock': 3, 'vendor_lead_time_days': 5, 'operational_criticality': 'CRITICAL_MEDIUM', 'unit_cost_inr': 16000},
    {'part_no': 'CC-PRT-RLR-03', 'part_name': 'Heavy Duty Carrying Idler Roller', 'current_stock': 10, 'vendor_lead_time_days': 3, 'operational_criticality': 'CRITICAL_MEDIUM', 'unit_cost_inr': 3500},
    {'part_no': 'CC-PRT-MTR-04', 'part_name': '110kW Drive Motor', 'current_stock': 1, 'vendor_lead_time_days': 16, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 210000},
    {'part_no': 'CC-PRT-GBX-05', 'part_name': 'Helical Speed Gearbox', 'current_stock': 0, 'vendor_lead_time_days': 20, 'operational_criticality': 'CRITICAL_HIGH', 'unit_cost_inr': 280000}
])

# ==========================================
# 4. UNSTRUCTURED MAINTENANCE LOGS (Table 4)
# Real-world plant logs matching failure symptoms for NLP/Gemini extraction.
# ==========================================
logs_df = pd.DataFrame([
    {
        'log_id': 'WO-2026-TPP-101',
        'asset_tag': 'BFP-01',
        'timestamp': (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d'),
        'technician_notes': 'Boiler feedwater pump discharge pressure dropped significantly to 65 bar. Slight fluid weeping near mechanical seal housing.',
        'maintenance_type': 'Unscheduled Inspection'
    },
    {
        'log_id': 'WO-2026-TPP-102',
        'asset_tag': 'ST-01',
        'timestamp': (datetime.today() - timedelta(days=4)).strftime('%Y-%m-%d'),
        'technician_notes': 'Steam turbine bearing housing vibrating heavily above 9 mm/s. Bearing temperature reaching 95C. Blade wear or rotor imbalance suspected.',
        'maintenance_type': 'Emergency Callout'
    },
    {
        'log_id': 'WO-2026-TPP-103',
        'asset_tag': 'GEN-01',
        'timestamp': (datetime.today() - timedelta(days=6)).strftime('%Y-%m-%d'),
        'technician_notes': 'Exciter voltage fluctuating. Stator winding temperature stable but hydrogen seal pressure reading low.',
        'maintenance_type': 'Preventive Maintenance'
    },
    {
        'log_id': 'WO-2026-TPP-104',
        'asset_tag': 'CWP-01',
        'timestamp': (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'),
        'technician_notes': 'Cooling water flow rate dropped slightly. Cavitation noises heard in the impeller housing.',
        'maintenance_type': 'Routine Check'
    },
    {
        'log_id': 'WO-2026-TPP-105',
        'asset_tag': 'CC-01',
        'timestamp': (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d'),
        'technician_notes': 'Coal conveyor belt showing severe edge fraying and tension loss. Drive motor current drawing 220A under normal load.',
        'maintenance_type': 'Unscheduled Inspection'
    }
])

# ==========================================
# 5. PRODUCTION SCHEDULES (Table 5)
# Tracks planned production runs to help determine operational downtime costs.
# ==========================================
schedules_df = pd.DataFrame([
    {
        'schedule_id': 'PROD-WK40-A',
        'asset_tag': 'BFP-01',
        'planned_start': (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'planned_end': (datetime.today() + timedelta(days=5)).strftime('%Y-%m-%d'),
        'production_target': 'High-Pressure Steam Generation',
        'downtime_cost_per_hour_inr': 150000 
    },
    {
        'schedule_id': 'PROD-WK40-B',
        'asset_tag': 'ST-01',
        'planned_start': (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'planned_end': (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
        'production_target': 'Base Load Power Export (500MW)',
        'downtime_cost_per_hour_inr': 500000
    },
    {
        'schedule_id': 'PROD-WK40-C',
        'asset_tag': 'CC-01',
        'planned_start': (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d'),
        'planned_end': (datetime.today() + timedelta(days=3)).strftime('%Y-%m-%d'),
        'production_target': 'Silo B Coal Replenishment',
        'downtime_cost_per_hour_inr': 75000
    }
])

schedules_df.to_csv('5_production_schedules.csv', index=False)
print("Table 5 (Production Schedules) generated successfully.")
# ==========================================
# EXPORT TO CSV
# ==========================================
telemetry_df.to_csv('1_telemetry_data.csv', index=False)
bom_df.to_csv('2_bom_mapping.csv', index=False)
inventory_df.to_csv('3_inventory_master.csv', index=False)
logs_df.to_csv('4_maintenance_logs.csv', index=False)

print("Thermal Power Plant Dataset Generation Complete!")
print("Generated 4 CSV files covering all 5 machines, signals, failure modes, and spare parts.")