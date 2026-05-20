from data import SYMPTOM_DATA

def recommend_medicine(symptom: str):
    symptom = symptom.lower().strip()
    for key in SYMPTOM_DATA:
        if key in symptom:
            d = SYMPTOM_DATA[key]
            return {
                "found": True,
                "symptom": key,
                "medicines": d["medicines"],
                "advice": d["advice"]
            }
    return {"found": False, "message": "Symptom not in database. Please consult a doctor."}

def suggest_doctor(symptom: str):
    symptom = symptom.lower().strip()
    for key in SYMPTOM_DATA:
        if key in symptom:
            return {
                "found": True,
                "symptom": key,
                "doctors": SYMPTOM_DATA[key]["doctors"]
            }
    return {"found": False, "message": "No specific doctor found. Visit a General Physician."}

TOOLS = {
    "recommend_medicine": recommend_medicine,
    "suggest_doctor": suggest_doctor,
}