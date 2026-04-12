from .client import get_database

async def init_indexes():
    db = get_database()
    
    # patients: patient_id is unique
    await db.patients.create_index("patient_id", unique=True)
    
    # chronic_diseases: disease_id is unique
    await db.chronic_diseases.create_index("disease_id", unique=True)
    
    # patient_diagnoses: diagnosis_id is unique, patient_id and disease_id are indexed
    await db.patient_diagnoses.create_index("diagnosis_id", unique=True)
    await db.patient_diagnoses.create_index("patient_id")
    await db.patient_diagnoses.create_index("disease_id")
    await db.patient_diagnoses.create_index("doctor_id")
    
    # clinical_metrics: metric_id is unique, diagnosis_id is indexed
    await db.clinical_metrics.create_index("metric_id", unique=True)
    await db.clinical_metrics.create_index("diagnosis_id")
    await db.clinical_metrics.create_index("doctor_id")
    
    # disease_episodes: episode_id is unique, diagnosis_id is indexed
    await db.disease_episodes.create_index("episode_id", unique=True)
    await db.disease_episodes.create_index("diagnosis_id")
    await db.disease_episodes.create_index("doctor_id")
    
    # risk_assessments: assessment_id is unique, patient_id is indexed
    await db.risk_assessments.create_index("assessment_id", unique=True)
    await db.risk_assessments.create_index("patient_id")
    
    # treatment_plans: plan_id is unique, diagnosis_id is indexed
    await db.treatment_plans.create_index("plan_id", unique=True)
    await db.treatment_plans.create_index("diagnosis_id")
    await db.treatment_plans.create_index("doctor_id")
    
    # medication_adherences: adherence_id is unique, plan_id is indexed
    await db.medication_adherences.create_index("adherence_id", unique=True)
    await db.medication_adherences.create_index("plan_id")
    
    print("Database indexes initialized")
