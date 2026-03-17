from database import get_database

db = get_database()

# ==========================================
# PATIENT OPERATIONS
# ==========================================

def create_patient(patient_data: dict) -> str:
    """
    Inserts a new patient into the 'Patients' collection.
    Expected keys: PatientID, Name, Age, Gender, ContactNumber, Address, EmergencyContact
    """
    collection = db["Patients"]
    result = collection.insert_one(patient_data)
    return str(result.inserted_id)

def get_all_patients() -> list:
    """
    Retrieves all patients.
    """
    collection = db["Patients"]
    return list(collection.find({}, {"_id": 0}))

def get_patient_by_id(patient_id: str) -> dict:
    """
    Retrieves a specific patient by their PatientID.
    """
    collection = db["Patients"]
    return collection.find_one({"PatientID": patient_id}, {"_id": 0})

def update_patient(patient_id: str, update_data: dict) -> int:
    """
    Updates a patient's information.
    """
    collection = db["Patients"]
    result = collection.update_one({"PatientID": patient_id}, {"$set": update_data})
    return result.modified_count

def delete_patient(patient_id: str) -> int:
    """
    Deletes a patient record.
    """
    collection = db["Patients"]
    result = collection.delete_one({"PatientID": patient_id})
    return result.deleted_count

# ==========================================
# DOCTOR OPERATIONS
# ==========================================

def create_doctor(doctor_data: dict) -> str:
    """
    Inserts a new doctor into the 'Doctors' collection.
    Expected keys: DoctorID, Name, Specialization, ContactNumber, Email, AssignedPatients (List)
    """
    collection = db["Doctors"]
    result = collection.insert_one(doctor_data)
    return str(result.inserted_id)

def get_all_doctors() -> list:
    """
    Retrieves all doctors.
    """
    collection = db["Doctors"]
    return list(collection.find({}, {"_id": 0}))

def get_doctor_by_id(doctor_id: str) -> dict:
    """
    Retrieves a specific doctor by DoctorID.
    """
    collection = db["Doctors"]
    return collection.find_one({"DoctorID": doctor_id}, {"_id": 0})

def update_doctor(doctor_id: str, update_data: dict) -> int:
    """
    Updates a doctor's information.
    """
    collection = db["Doctors"]
    result = collection.update_one({"DoctorID": doctor_id}, {"$set": update_data})
    return result.modified_count

# ==========================================
# CONDITION (DISEASE) OPERATIONS
# ==========================================

def create_condition(condition_data: dict) -> str:
    """
    Inserts a new chronic condition type into the 'Conditions' collection.
    Expected keys: ConditionID, ConditionName, Description, TypicalSymptoms, StandardTreatments
    """
    collection = db["Conditions"]
    result = collection.insert_one(condition_data)
    return str(result.inserted_id)

def get_all_conditions() -> list:
    """
    Retrieves all stored conditions/diseases.
    """
    collection = db["Conditions"]
    return list(collection.find({}, {"_id": 0}))

# ==========================================
# TREATMENT PLAN OPERATIONS
# ==========================================

def create_treatment_plan(plan_data: dict) -> str:
    """
    Inserts a new treatment plan for a patient.
    Expected keys: PlanID, PatientID, DoctorID, ConditionID, StartDate, EndDate, Medications, LifestyleChanges, NextReviewDate
    """
    collection = db["TreatmentPlans"]
    result = collection.insert_one(plan_data)
    return str(result.inserted_id)

def get_treatment_plans_for_patient(patient_id: str) -> list:
    """
    Retrieves all treatment plans for a specific patient.
    """
    collection = db["TreatmentPlans"]
    return list(collection.find({"PatientID": patient_id}, {"_id": 0}))

def update_treatment_plan(plan_id: str, update_data: dict) -> int:
    """
    Updates a treatment plan.
    """
    collection = db["TreatmentPlans"]
    result = collection.update_one({"PlanID": plan_id}, {"$set": update_data})
    return result.modified_count

# ==========================================
# APPOINTMENT / RECORD OPERATIONS
# ==========================================

def create_appointment(appointment_data: dict) -> str:
    """
    Inserts a new appointment record.
    Expected keys: AppointmentID, PatientID, DoctorID, DateTime, Purpose, Notes, Status
    """
    collection = db["Appointments"]
    result = collection.insert_one(appointment_data)
    return str(result.inserted_id)

def get_appointments_for_patient(patient_id: str) -> list:
    """
    Retrieves all appointments for a specific patient.
    """
    collection = db["Appointments"]
    return list(collection.find({"PatientID": patient_id}, {"_id": 0}))

def get_appointments_for_doctor(doctor_id: str) -> list:
    """
    Retrieves all appointments for a specific doctor.
    """
    collection = db["Appointments"]
    return list(collection.find({"DoctorID": doctor_id}, {"_id": 0}))

def update_appointment_status(appointment_id: str, status: str) -> int:
    """
    Updates the status of an appointment (e.g., 'Scheduled', 'Completed', 'Cancelled').
    """
    collection = db["Appointments"]
    result = collection.update_one({"AppointmentID": appointment_id}, {"$set": {"Status": status}})
    return result.modified_count

# ==========================================
# TEST BLOCK (To verify it works)
# ==========================================

if __name__ == "__main__":
    print("Testing CRUD operations module...")
    
    # 1. Test basic read operation to ensure connection works
    try:
        patients = get_all_patients()
        print(f"Success! Retrieved {len(patients)} patients from the database.")
    except Exception as e:
        print(f"Error during CRUD test: {e}")