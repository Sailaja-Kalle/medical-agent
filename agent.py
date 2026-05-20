import requests
import json
from tools import TOOLS

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

SYSTEM_PROMPT = """You are a smart medical assistant agent.
When a user describes a symptom or disease, extract the best matching keyword.
Reply ONLY in valid JSON format (no extra text, no explanation):
{
  "tool": "recommend_medicine",
  "symptom": "fever"
}
Available tools: recommend_medicine, suggest_doctor
Known symptom keywords: fever, headache, cough, cold, chest pain, stomach pain, 
back pain, cancer, diabetes, blood pressure, asthma, thyroid, migraine, 
skin rash, eye pain, tooth pain, anxiety, depression, kidney pain, joint pain
If the symptom is not in the list, still return the closest matching keyword."""

def run_agent(user_input: str):
    payload = {
        "model": MODEL,
        "prompt": SYSTEM_PROMPT + "\n\nUser says: " + user_input,
        "stream": False
    }
    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=60)
        raw = res.json().get("response", "").strip()
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