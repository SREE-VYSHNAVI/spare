import json
from typing import Dict, Any

def ask_sparewise_assistant(query: str, context: Dict[str, Any]) -> str:
    """
    SpareWise AI Assistant - Conversational interface for maintenance queries
    """
    query_lower = query.lower()
    
    # Extract context
    summary = context.get('summary', {})
    inventory = context.get('inventory', [])
    
    # Critical parts check
    critical_parts = [item for item in inventory if item.get('current_stock', 0) == 0]
    
    # Define response patterns
    if any(word in query_lower for word in ['critical', 'alert', 'urgent', 'emergency']):
        if critical_parts:
            part_names = ', '.join([p.get('part_name', p.get('part_no', 'Unknown')) for p in critical_parts[:3]])
            return f"⚠️ CRITICAL: {len(critical_parts)} parts are out of stock! Most urgent: {part_names}. Recommend emergency procurement immediately."
        return "No critical stock issues detected at the moment."
    
    if any(word in query_lower for word in ['inventory', 'stock', 'parts']):
        total_stock = sum(item.get('current_stock', 0) for item in inventory)
        return f"📦 Current Inventory Status:\n- Total parts in stock: {total_stock}\n- Critical shortages: {len(critical_parts)}\n- Total part types: {len(inventory)}\n\nRecommend immediate procurement for {len(critical_parts)} critical parts."
    
    if any(word in query_lower for word in ['lead time', 'delivery', 'when', 'how long']):
        if inventory:
            avg_lead_time = sum(item.get('vendor_lead_time_days', 0) for item in inventory) / len(inventory)
            return f"⏱️ Average Lead Time Analysis:\n- Average delivery time: {avg_lead_time:.1f} days\n- Fastest parts: 3-5 days\n- Longest lead times: 20-30 days\n\nPlan procurement accordingly for critical equipment."
        return "Lead time data not available."
    
    if any(word in query_lower for word in ['recommend', 'suggest', 'advise', 'should']):
        return "💡 Recommendations:\n1. Maintain minimum stock levels for CRITICAL_HIGH priority parts\n2. Pre-order long lead-time items (>20 days)\n3. Monitor bearing temperatures and vibration levels\n4. Schedule preventive maintenance during low-load periods\n5. Establish vendor relationships for emergency orders."
    
    if any(word in query_lower for word in ['failure', 'breakdown', 'risk', 'predict']):
        return "🔍 Predictive Maintenance:\n- Monitor bearing temperature (normal: <70°C)\n- Track vibration levels (normal: <3 mm/s)\n- Motor current should stay below 170A\n- Pressure anomalies indicate seal/bearing issues\n\nUse sensor data to predict failures 5-10 days in advance."
    
    if any(word in query_lower for word in ['asset', 'machine', 'equipment', 'pump', 'turbine', 'generator', 'conveyor']):
        return "🏭 Thermal Power Plant Assets:\n1. BFP-01: Boiler Feedwater Pump\n2. ST-01: Steam Turbine\n3. GEN-01: Generator\n4. CWP-01: Cooling Water Pump\n5. CC-01: Coal Conveyor\n\nEach asset has specific failure modes and spare parts. Use the Failure Prediction tool for detailed analysis."
    
    if any(word in query_lower for word in ['cost', 'price', 'expensive', 'budget']):
        total_cost = sum(item.get('unit_cost_inr', 0) * item.get('current_stock', 0) for item in inventory)
        return f"💰 Cost Analysis:\n- Current inventory value: ₹{total_cost:,.0f}\n- Highest cost item: Generator parts (₹320,000+)\n- Recommend optimizing stock levels to balance availability vs. cost."
    
    # Default helpful response
    return "👋 Hello! I'm SpareWise AI Assistant. I can help with:\n- Inventory status and stock levels\n- Lead time predictions\n- Failure risk assessment\n- Maintenance recommendations\n- Cost analysis\n\nTry asking about specific concerns or assets!"  
