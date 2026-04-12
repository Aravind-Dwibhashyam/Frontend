import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from db.client import settings
from datetime import date, datetime, timedelta

async def seed_db():
    print(f"Connecting to {settings.MONGO_URI}...")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    
    # Let's use a fresh database name for testing
    db = client.chronic_care
    
    # Drop existing dev data if any
    await db.patients.drop()
    await db.chronic_diseases.drop()
    await db.patient_diagnoses.drop()
    await db.clinical_metrics.drop()
    await db.disease_episodes.drop()
    await db.risk_assessments.drop()
    await db.treatment_plans.drop()
    await db.medication_adherences.drop()
    await db.integration_logs.drop()
    
    print("Dropped old collections, seeding new data...")

    # Insert Patients
    patients = [
        {"patient_id": "PT-001", "name": "John Doe", "dob": "1960-05-14", "age": 63, "gender": "Male"},
        {"patient_id": "PT-002", "name": "Jane Smith", "dob": "1955-08-21", "age": 68, "gender": "Female"},
        {"patient_id": "PT-003", "name": "Robert Johnson", "dob": "1972-11-03", "age": 51, "gender": "Male"}
    ]
    await db.patients.insert_many(patients)

    # Insert Chronic Diseases
    diseases = [
        {"disease_id": "DIS-DB", "name": "Type 2 Diabetes", "type": "Metabolic", "description": "Chronic condition affecting metabolism of sugar"},
        {"disease_id": "DIS-HT", "name": "Hypertension", "type": "Cardiovascular", "description": "Consistently high blood pressure"},
        {"disease_id": "DIS-COPD", "name": "COPD", "type": "Respiratory", "description": "Chronic obstructive pulmonary disease"}
    ]
    await db.chronic_diseases.insert_many(diseases)

    # Insert Patient Diagnoses
    diagnoses = [
        {"diagnosis_id": "DGN-101", "patient_id": "PT-001", "disease_id": "DIS-DB", "date_diagnosed": "2015-06-10", "severity_stage": "Moderate", "current_status": "Active", "doctor_id": "DOC-999"},
        {"diagnosis_id": "DGN-102", "patient_id": "PT-001", "disease_id": "DIS-HT", "date_diagnosed": "2018-09-12", "severity_stage": "Mild", "current_status": "Active", "doctor_id": "DOC-999"},
        {"diagnosis_id": "DGN-103", "patient_id": "PT-002", "disease_id": "DIS-COPD", "date_diagnosed": "2020-03-05", "severity_stage": "Severe", "current_status": "Active", "doctor_id": "DOC-800"}
    ]
    await db.patient_diagnoses.insert_many(diagnoses)

    # Insert Clinical Metrics
    metrics = [
        {"metric_id": "MET-01", "diagnosis_id": "DGN-101", "metric_type": "HbA1c", "value": 7.5, "unit": "%", "recorded_at": datetime.utcnow().isoformat(), "doctor_id": "DOC-999"},
        {"metric_id": "MET-02", "diagnosis_id": "DGN-102", "metric_type": "Blood Pressure", "value": 140, "unit": "mmHg Sys", "recorded_at": datetime.utcnow().isoformat(), "doctor_id": "DOC-999"}
    ]
    await db.clinical_metrics.insert_many(metrics)

    # Insert Risk Assessments
    risks = [
        {"assessment_id": "RSK-01", "patient_id": "PT-001", "risk_score": 75.5, "category": "High"},
        {"assessment_id": "RSK-02", "patient_id": "PT-002", "risk_score": 88.0, "category": "Critical"},
        {"assessment_id": "RSK-03", "patient_id": "PT-003", "risk_score": 45.0, "category": "Moderate"}
    ]
    await db.risk_assessments.insert_many(risks)

    # Insert Disease Episodes
    episodes = [
        {"episode_id": "EP-001", "diagnosis_id": "DGN-101", "start_date": "2023-01-10", "end_date": "2023-01-15", "severity_levels": "High", "triggers": ["Diet", "Stress"], "doctor_id": "DOC-999"},
        {"episode_id": "EP-002", "diagnosis_id": "DGN-103", "start_date": "2023-11-20", "end_date": None, "severity_levels": "Critical", "triggers": ["Weather", "Pollution"], "doctor_id": "DOC-800"}
    ]
    await db.disease_episodes.insert_many(episodes)

    # Insert Treatment Plans
    plans = [
        {"plan_id": "PLN-A1", "diagnosis_id": "DGN-101", "goal": "Maintain HbA1c below 7%", "start_date": "2023-02-01", "doctor_id": "DOC-999"},
        {"plan_id": "PLN-B1", "diagnosis_id": "DGN-102", "goal": "Keep BP below 130/80", "start_date": "2023-05-15", "doctor_id": "DOC-999"}
    ]
    await db.treatment_plans.insert_many(plans)

    # Insert Medication Adherences
    adherences = [
        {"adherence_id": "ADH-001", "plan_id": "PLN-A1", "log_date": (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d'), "status": "Taken", "reason_skipped": None},
        {"adherence_id": "ADH-002", "plan_id": "PLN-A1", "log_date": datetime.utcnow().strftime('%Y-%m-%d'), "status": "Skipped", "reason_skipped": "Forgot"}
    ]
    await db.medication_adherences.insert_many(adherences)

    print("Successfully seeded dummy data into 'chronic_care' database!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_db())
