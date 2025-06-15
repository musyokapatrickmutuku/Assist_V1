PATIENT_DATA = {
    "P001": {
        "profile": {
            "Patient ID": "P001",
            "Age at Diagnosis": "45 years",
            "Gender": "Female",
            "Ethnicity": "African American",
            "Type of Diabetes": "Type 2",
            "Initial Symptoms": "Excessive thirst, frequent urination, blurred vision, unexplained 15-pound weight loss over 3 months",
            "Family History": "Mother-Type 2, Maternal grandmother-Type 2",
            "Co-morbidities at Diagnosis": "Hypertension, Obesity (BMI 32.4), Dyslipidemia",
            "Lifestyle at Diagnosis": "Sedentary office job, high-carbohydrate diet, non-smoker, occasional social drinking"
        },
        "baseline_diagnostic_info": {
            "HbA1c": "9.8%",
            "Fasting Blood Glucose": "245 mg/dL",
            "Random Blood Glucose": "320 mg/dL",
            "C-peptide": "Normal (2.8 ng/mL)",
            "Lipid Panel": "Total Cholesterol 235 mg/dL, LDL-C 155 mg/dL, HDL-C 38 mg/dL, Triglycerides 220 mg/dL",
            "Kidney Function": "eGFR 85 mL/min/1.73m², UACR 25 mg/g",
            "Blood Pressure": "148/92 mmHg",
            "Weight & Height": "88 kg, 165 cm"
        },
        "longitudinal_progress": [
            {
                "date": "15-03-2022",
                "type": "Initial Consultation",
                "Health Status": "Symptomatic with polyuria, polydipsia, fatigue",
                "Lab Values": "HbA1c 9.8%, FBG 245 mg/dL, BP 148/92 mmHg, Weight 88 kg",
                "Medications": "Metformin 1000mg BID, Lisinopril 10mg daily",
                "Duration": "Initial prescription, 3-month follow-up planned",
                "Lifestyle Recommendations": "Dietary counseling, gradual exercise introduction, blood glucose monitoring"
            },
            {
                "date": "20-06-2022",
                "type": "3-Month Follow-up",
                "Health Status": "Significant symptom improvement, 8-pound weight loss, mild GI upset from metformin",
                "Lab Values": "HbA1c 8.1%, Average FBG 165 mg/dL, BP 138/85 mmHg, Weight 80 kg",
                "Medications": "Continue Metformin 1000mg BID, increase Lisinopril to 15mg daily",
                "Duration": "Ongoing, 3-month follow-up",
                "Lifestyle Recommendations": "Continue current diet plan, increase walking to 45 minutes daily",
                "Reason for Change": "Good response to initial therapy, BP still elevated"
            },
            {
                "date": "18-09-2022",
                "type": "6-Month Follow-up",
                "Health Status": "Stable, experiencing occasional mild hypoglycemia, improved energy",
                "Lab Values": "HbA1c 7.4%, Average FBG 140 mg/dL, BP 132/80 mmHg, Weight 78 kg, eGFR 88 mL/min/1.73m²",
                "Medications": "Continue current regimen, add Empagliflozin 10mg daily",
                "Duration": "6-month trial",
                "Lifestyle Recommendations": "Hypoglycemia education, continue current exercise routine",
                "Reason for Change": "Approaching target but need additional cardiovascular protection"
            }
        ]
    },
    "P002": {
        "profile": {
            "Patient ID": "P002",
            "Age at Diagnosis": "16 years",
            "Gender": "Male",
            "Ethnicity": "Caucasian",
            "Type of Diabetes": "Type 1",
            "Initial Symptoms": "Rapid 20-pound weight loss, severe fatigue, extreme thirst, frequent urination, fruity breath odor",
            "Family History": "No known family history of diabetes",
            "Co-morbidities at Diagnosis": "None",
            "Lifestyle at Diagnosis": "Active high school athlete (soccer), healthy diet, non-smoker"
        },
        "baseline_diagnostic_info": {
            "HbA1c": "12.5%",
            "Fasting Blood Glucose": "385 mg/dL",
            "Random Blood Glucose": "445 mg/dL",
            "C-peptide": "Very low (0.3 ng/mL)",
            "Autoantibodies": "GAD65 positive, ICA positive",
            "Lipid Panel": "Total Cholesterol 165 mg/dL, LDL-C 95 mg/dL, HDL-C 52 mg/dL, Triglycerides 120 mg/dL",
            "Kidney Function": "eGFR >90 mL/min/1.73m², UACR 8 mg/g",
            "Blood Pressure": "118/72 mmHg",
            "Weight & Height": "58 kg, 175 cm"
        },
        "longitudinal_progress": [
            {
                "date": "08-09-2021",
                "type": "Initial Diagnosis/Hospitalization",
                "Health Status": "Admitted with DKA, ketones 4.2 mmol/L, pH 7.15",
                "Lab Values": "HbA1c 12.5%, Random BG 445 mg/dL, BP 118/72 mmHg, Weight 58 kg",
                "Medications": "IV insulin infusion initially, then Insulin Aspart 6 units TID with meals, Insulin Glargine 12 units at bedtime",
                "Duration": "Hospital stay 4 days, intensive diabetes education",
                "Lifestyle Recommendations": "Carb counting education, glucose monitoring 4x daily, gradual return to sports"
            },
            {
                "date": "10-10-2021",
                "type": "1-Month Follow-up",
                "Health Status": "Adjusting to insulin therapy, frequent BG monitoring, honeymoon phase beginning",
                "Lab Values": "HbA1c 9.2%, Average FBG 145 mg/dL, BP 115/70 mmHg, Weight 62 kg",
                "Medications": "Reduce Insulin Aspart to 4 units TID, reduce Glargine to 8 units",
                "Duration": "Ongoing adjustments expected",
                "Lifestyle Recommendations": "Continue intensive monitoring, return to soccer with precautions",
                "Reason for Change": "Honeymoon phase reducing insulin requirements"
            },
            {
                "date": "15-03-2022",
                "type": "6-Month Follow-up",
                "Health Status": "Honeymoon phase ending, more insulin needed, good diabetes management skills",
                "Lab Values": "HbA1c 7.1%, Average FBG 135 mg/dL, BP 120/75 mmHg, Weight 68 kg",
                "Medications": "Increase Insulin Aspart to 8 units TID, increase Glargine to 18 units",
                "Duration": "Ongoing with monthly adjustments",
                "Lifestyle Recommendations": "Continue carb counting, exercise management education"
            }
        ]
    }
}

def get_patient_data(patient_id):
    return PATIENT_DATA.get(patient_id)