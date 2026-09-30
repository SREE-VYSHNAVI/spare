import os
import google.generativeai as genai

# Configure Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def ask_sparewise_assistant(user_query: str, plant_context: dict) -> str:
    if not GEMINI_API_KEY:
        return (
            f"Mock AI Response: Regarding your query ('{user_query}'), "
            f"the system notes that BFP-01 is at high risk of failure due to seal degradation, "
            f"and current inventory for part BFP-PRT-SEAL-02 is at 0 units with a 6-day lead time."
        )
    
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = f"""
        You are SpareWise AI, an expert assistant for a Thermal Power Plant maintenance manager.
        Use the following live plant data context to answer the user's question accurately. Do not invent numbers.
        
        Plant Context: {plant_context}
        
        User Question: {user_query}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini API: {str(e)}"