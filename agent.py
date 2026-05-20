import requests
import json
import os
from tools import TOOLS
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

SYSTEM_PROMPT = """You are a smart medical assistant agent.
When a user describes a symptom or disease, extract the best matching keyword.
Reply ONLY in valid JSON format:
{
  "tool": "recommend_medicine",
  "symptom": "fever"
}
Known keywords: fever, headache, cough, cold, chest pain, stomach pain,
back pain, cancer, diabetes, blood pressure, asthma, thyroid, migraine,
skin rash, eye pain, tooth pain, anxiety, depression, kidney pain, joint pain"""

def run_agent(user_input: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    }
    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        raw = res.json()["choices"][0]["message"]["content"].strip()
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end != 0:
            parsed = json.loads(raw[start:end])
            tool_name = parsed.get("tool")
            symptom = parsed.get("symptom", user_input)
            if tool_name in TOOLS:
                result = TOOLS[tool_name](symptom)
                doctor_result = TOOLS["suggest_doctor"](symptom)
                if result.get("found"):
                    return {
                        "status": "success",
                        "symptom_detected": symptom,
                        "medicines": result.get("medicines", []),
                        "advice": result.get("advice", ""),
                        "doctors": doctor_result.get("doctors", [])
                    }
    except Exception as e:
        pass

    med = TOOLS["recommend_medicine"](user_input)
    doc = TOOLS["suggest_doctor"](user_input)

    if not med.get("found"):
        return {
            "status": "not_found",
            "symptom_detected": user_input,
            "medicines": ["No specific medicine found — please consult a doctor"],
            "advice": "This symptom is not in our database. Please visit a qualified doctor.",
            "doctors": ["General Physician"]
        }

    return {
        "status": "success",
        "symptom_detected": user_input,
        "medicines": med.get("medicines", []),
        "advice": med.get("advice", "Consult a doctor for proper diagnosis."),
        "doctors": doc.get("doctors", ["General Physician"])
    }