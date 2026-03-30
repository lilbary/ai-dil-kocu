import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


model = genai.GenerativeModel('gemini-flash-latest')

def get_ai_feedback(user_input: str):
    prompt = f"Sen bir İngilizce koçusun. Şu cümleyi analiz et ve Türkçe geri bildirim ver: {user_input}"
    
    
    response = model.generate_content(prompt)
    return response.text