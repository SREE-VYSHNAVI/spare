import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)

# Generate 500 past orders to train the supply chain model
num_orders = 500
parts = ['BFP-PRT-BRG-01', 'ST-PRT-BLD-02', 'CWP-PRT-IMP-03', 'CC-PRT-BLT-01']
seasons = ['Summer', 'Monsoon', 'Winter']
market_conditions = ['Normal', 'High Demand (Shortage)']

data = []
today = datetime.today()

for i in range(num_orders):
    part = random.choice(parts)
    season = random.choice(seasons)
    market = random.choice(market_conditions)
    
    # Base promised lead time
    base_lead_time = 10 if part == 'BFP-PRT-BRG-01' else (30 if part == 'ST-PRT-BLD-02' else 14)
    
    # Inject real-world delays
    actual_lead_time = base_lead_time
    
    # Monsoons cause logistics and shipping delays
    if season == 'Monsoon':
        actual_lead_time += np.random.randint(3, 8) 
        
    # High demand causes factory backorders
    if market == 'High Demand (Shortage)':
        actual_lead_time += np.random.randint(5, 15)
        
    # Standard random shipping variance (+/- 2 days)
    actual_lead_time += np.random.randint(-2, 3)
    
    data.append({
        'order_id': f"ORD-{1000+i}",
        'part_no': part,
        'season': season,
        'market_condition': market,
        'promised_lead_time_days': base_lead_time,
        'actual_delivery_days': max(1, actual_lead_time) # Model Target Variable
    })

supply_df = pd.DataFrame(data)
supply_df.to_csv('6_supply_chain_history.csv', index=False)
print("Historical supply chain dataset generated successfully.")