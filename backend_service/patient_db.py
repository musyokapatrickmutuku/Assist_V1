# backend_service/patient_db.py
import sqlite3
import os
from datetime import datetime

DB_PATH = os.environ.get('DB_PATH', 'queries.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create queries table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS queries (
        id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        patient_id TEXT NOT NULL,
        original_query TEXT NOT NULL,
        ai_response TEXT,
        doctor_final_response TEXT,
        status TEXT NOT NULL,
        urgency_level TEXT DEFAULT 'low',
        safety_score INTEGER,
        confidence_score INTEGER
    )
    """)
    
    conn.commit()
    conn.close()

# Initialize database on import
if __name__ == "__main__":
    init_db()

def get_patient_data(patient_id):
    """
    Returns comprehensive patient data for demo purposes.
    In production, this would fetch from a real patient database.
    """
    patients = {
        "P001": {
            "profile": {
                "patient_id": "P001",
                "name": "Sarah Johnson",
                "age": 47,
                "gender": "Female",
                "ethnicity": "African American",
                "Type of Diabetes": "Type 2",
                "diagnosis_date": "2022-03-15",
                "years_since_diagnosis": 2.5
            },
            "current_status": {
                "hba1c": "6.9%",
                "last_fasting_glucose": "130 mg/dL",
                "blood_pressure": "125/75 mmHg",
                "weight": "76 kg",
                "bmi": 27.9,
                "kidney_function": "eGFR 90 mL/min/1.73m²"
            },
            "medications": [
                {"name": "Metformin", "dose": "1000mg BID", "duration": "2.5 years"},
                {"name": "Lisinopril", "dose": "15mg daily", "duration": "2.5 years"},
                {"name": "Empagliflozin", "dose": "10mg daily", "duration": "2 years"}
            ],
            "complications": {
                "retinopathy": "None",
                "neuropathy": "None",
                "nephropathy": "Normal kidney function"
            },
            "lifestyle": {
                "exercise": "45 minutes daily walking",
                "diet": "Low-carb, following meal plan",
                "smoking": "Non-smoker",
                "alcohol": "Occasional social drinking"
            },
            "family_history": ["Mother - Type 2", "Maternal grandmother - Type 2"],
            "last_visit": "2024-03-15",
            "next_appointment": "2024-09-15",
            "care_team": {
                "primary": "Dr. Emily Chen",
                "endocrinologist": "Dr. Michael Roberts",
                "dietitian": "Jane Smith, RD"
            }
        },
        
        "P002": {
            "profile": {
                "patient_id": "P002",
                "name": "Michael Thompson",
                "age": 19,
                "gender": "Male",
                "ethnicity": "Caucasian",
                "Type of Diabetes": "Type 1",
                "diagnosis_date": "2021-09-08",
                "years_since_diagnosis": 3
            },
            "current_status": {
                "hba1c": "7.8%",
                "last_fasting_glucose": "155 mg/dL",
                "blood_pressure": "122/78 mmHg",
                "weight": "78 kg",
                "bmi": 25.5,
                "kidney_function": "eGFR >90 mL/min/1.73m²"
            },
            "medications": [
                {"name": "Insulin Pump (Aspart)", "dose": "Basal 1.2 units/hour", "duration": "6 months"},
                {"name": "Previous: Insulin Glargine", "dose": "22 units at bedtime", "duration": "2.5 years (discontinued)"}
            ],
            "complications": {
                "retinopathy": "None",
                "neuropathy": "None",
                "nephropathy": "Normal kidney function"
            },
            "lifestyle": {
                "exercise": "College soccer team, daily training",
                "diet": "Carb counting, flexible with pump",
                "smoking": "Non-smoker",
                "alcohol": "Occasional (college student)"
            },
            "family_history": ["No family history of diabetes"],
            "last_visit": "2024-09-20",
            "next_appointment": "2024-12-20",
            "special_notes": "Recently started college, adjusting to new schedule"
        },
        
        "P003": {
            "profile": {
                "patient_id": "P003",
                "name": "Carlos Rodriguez",
                "age": 64,
                "gender": "Male",
                "ethnicity": "Hispanic",
                "Type of Diabetes": "Type 2",
                "diagnosis_date": "2022-04-12",
                "years_since_diagnosis": 2.5
            },
            "current_status": {
                "hba1c": "6.8%",
                "last_fasting_glucose": "132 mg/dL",
                "blood_pressure": "125/78 mmHg",
                "weight": "80 kg",
                "bmi": 27.0,
                "kidney_function": "eGFR 64 mL/min/1.73m²"
            },
            "medications": [
                {"name": "Metformin", "dose": "1000mg BID", "duration": "2.5 years"},
                {"name": "Lisinopril", "dose": "20mg daily", "duration": "2.5 years"},
                {"name": "Empagliflozin", "dose": "10mg daily", "duration": "2.5 years"},
                {"name": "Semaglutide", "dose": "1mg weekly", "duration": "1.5 years"}
            ],
            "complications": {
                "retinopathy": "Mild NPDR - stable",
                "neuropathy": "None",
                "nephropathy": "Stage 2 CKD"
            },
            "comorbidities": ["CAD (prior MI 2020)", "Hypertension", "Dyslipidemia"],
            "lifestyle": {
                "exercise": "Daily walking 30 minutes",
                "diet": "Modified traditional Mexican diet",
                "smoking": "Former smoker (quit 2014)",
                "alcohol": "None"
            },
            "family_history": ["Father - Type 2", "Brother - Type 2"],
            "last_visit": "2024-04-15",
            "next_appointment": "2025-04-15"
        },
        
        "P004": {
            "profile": {
                "patient_id": "P004",
                "name": "Priya Patel",
                "age": 30,
                "gender": "Female",
                "ethnicity": "South Asian",
                "Type of Diabetes": "Type 2 (post-GDM)",
                "diagnosis_date": "2023-08-28",
                "years_since_diagnosis": 1
            },
            "current_status": {
                "hba1c": "6.2%",
                "last_fasting_glucose": "110 mg/dL",
                "blood_pressure": "128/78 mmHg",
                "weight": "72 kg",
                "bmi": 28.1,
                "kidney_function": "eGFR >90 mL/min/1.73m²",
                "pregnancy_status": "First trimester - second pregnancy"
            },
            "medications": [
                {"name": "Prenatal vitamins", "dose": "Daily", "duration": "Current"},
                {"name": "Metformin", "dose": "Discontinued for pregnancy", "duration": "Was 1000mg BID"}
            ],
            "complications": {
                "retinopathy": "None",
                "neuropathy": "None",
                "nephropathy": "Normal kidney function"
            },
            "comorbidities": ["PCOS", "History of GDM"],
            "lifestyle": {
                "exercise": "Prenatal yoga 3x/week",
                "diet": "Gestational diabetes meal plan",
                "smoking": "Non-smoker",
                "alcohol": "None (pregnancy)"
            },
            "family_history": ["Mother - Type 2", "Paternal grandfather - Type 2"],
            "obstetric_history": {
                "previous_pregnancies": 1,
                "gdm_in_previous": "Yes",
                "current_pregnancy_week": 8
            },
            "last_visit": "2024-08-15",
            "next_appointment": "2024-09-15"
        },
        
        "P005": {
            "profile": {
                "patient_id": "P005",
                "name": "Eleanor Williams",
                "age": 72,
                "gender": "Female",
                "ethnicity": "Caucasian",
                "Type of Diabetes": "Type 2",
                "diagnosis_date": "2023-01-10",
                "years_since_diagnosis": 1.5
            },
            "current_status": {
                "hba1c": "8.0%",
                "last_fasting_glucose": "170 mg/dL",
                "blood_pressure": "135/78 mmHg",
                "weight": "67 kg",
                "bmi": 25.5,
                "kidney_function": "eGFR 35 mL/min/1.73m² (CKD Stage 3b)"
            },
            "medications": [
                {"name": "Insulin Glargine", "dose": "18 units at bedtime", "duration": "1.5 years"},
                {"name": "Linagliptin", "dose": "5mg daily", "duration": "6 months"}
            ],
            "complications": {
                "retinopathy": "Mild NPDR",
                "neuropathy": "Peripheral neuropathy present",
                "nephropathy": "CKD Stage 3b"
            },
            "comorbidities": [
                "Hypertension",
                "Osteoarthritis",
                "Mild cognitive impairment",
                "CKD Stage 3b"
            ],
            "lifestyle": {
                "exercise": "Limited mobility, chair exercises",
                "diet": "Simplified meal plan with family help",
                "smoking": "Non-smoker",
                "alcohol": "None",
                "living_situation": "Lives alone, considering assisted living"
            },
            "family_history": ["Sister - Type 2"],
            "care_considerations": [
                "Cognitive impairment affecting compliance",
                "Family heavily involved in care",
                "Focus on avoiding hypoglycemia",
                "Simplified management approach"
            ],
            "last_visit": "2024-07-22",
            "next_appointment": "2024-10-22"
        }
    }
    
    return patients.get(patient_id)

def get_patient_summary(patient_id):
    """
    Returns a brief summary for quick reference in the UI
    """
    data = get_patient_data(patient_id)
    if not data:
        return None
    
    profile = data['profile']
    status = data['current_status']
    
    return {
        "name": profile.get('name', 'Unknown'),
        "diabetes_type": profile.get('Type of Diabetes'),
        "current_hba1c": status.get('hba1c'),
        "years_with_diabetes": profile.get('years_since_diagnosis'),
        "key_medications": len(data.get('medications', [])),
        "complications": any(v != "None" and v != "Normal kidney function" 
                           for v in data.get('complications', {}).values())
    }

def get_all_patients():
    """
    Returns a list of all available patient IDs and names for demo purposes
    """
    return [
        {"id": "P001", "name": "Sarah Johnson", "type": "Type 2"},
        {"id": "P002", "name": "Michael Thompson", "type": "Type 1"},
        {"id": "P003", "name": "Carlos Rodriguez", "type": "Type 2"},
        {"id": "P004", "name": "Priya Patel", "type": "Type 2 (post-GDM)"},
        {"id": "P005", "name": "Eleanor Williams", "type": "Type 2"}
    ]

# Demo-specific functions for hackathon
def get_patient_context_for_ai(patient_id):
    """
    Formats patient data specifically for AI context
    """
    data = get_patient_data(patient_id)
    if not data:
        return "No patient data available."
    
    profile = data['profile']
    status = data['current_status']
    meds = data.get('medications', [])
    
    context = f"""
    Patient: {profile.get('name')} ({profile.get('age')} year old {profile.get('gender')})
    Diabetes Type: {profile.get('Type of Diabetes')}
    Years since diagnosis: {profile.get('years_since_diagnosis')}
    Current HbA1c: {status.get('hba1c')}
    Last Glucose: {status.get('last_fasting_glucose')}
    
    Current Medications:
    {chr(10).join([f"- {m['name']}: {m['dose']}" for m in meds])}
    
    Key Complications: {', '.join([k + ': ' + v for k, v in data.get('complications', {}).items() if v != 'None'])}
    """
    
    # Add special considerations
    if patient_id == "P004":
        context += "\nIMPORTANT: Patient is currently pregnant (first trimester)"
    elif patient_id == "P005":
        context += "\nIMPORTANT: Patient has cognitive impairment and CKD Stage 3b"
    
    return context