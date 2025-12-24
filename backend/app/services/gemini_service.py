import google.generativeai as genai
import json
from app.core.config import settings

class GeminiService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None
            print("WARNING: GEMINI_API_KEY not set. AI features will not work.")

    async def generate_report(self, business_idea: str) -> dict:
        if not self.model:
            return {"error": "API Key missing"}

        prompt = f"""
        Act as a business consultant. Analyze the following business idea: "{business_idea}".
        Return the response strictly in this JSON format:
        {{
            "feasibility_score": <0-100>,
            "summary": "<2-3 sentences>",
            "pros": ["<pro1>", "<pro2>", ...],
            "cons": ["<con1>", "<con2>", ...],
            "economic_analysis": "<paragraph about market potential>"
        }}
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            # Clean response if necessary (remove markdown backticks)
            text = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(text)
        except Exception as e:
            print(f"Gemini Error: {e}")
            return {"error": str(e)}

gemini_service = GeminiService()
