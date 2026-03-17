import streamlit as st
import pandas as pd
import crud

# Set the page configuration
st.set_page_config(
    page_title="Chronic Disease Management module",
    page_icon="🏥",
    layout="wide"
)

# Main Title
st.title("🏥 Chronic Disease Patient Record Management")
st.markdown("---")

# Navigation Sidebar
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Manage Patients", "Manage Doctors", "Conditions"]
)

if menu == "Dashboard":
    st.header("Dashboard Overview")
    
    col1, col2, col3 = st.columns(3)
    
    patients = crud.get_all_patients()
    doctors = crud.get_all_doctors()
    conditions = crud.get_all_conditions()
    
    col1.metric("Total Patients", len(patients))
    col2.metric("Total Doctors", len(doctors))
    col3.metric("Monitored Conditions", len(conditions))
    
    st.subheader("Recent Patients")
    if patients:
        df_patients = pd.DataFrame(patients)
        # Reorder/select columns to show
        if "PatientID" in df_patients.columns and "Name" in df_patients.columns:
            st.dataframe(df_patients[["PatientID", "Name", "Age", "Gender", "ContactNumber"]], use_container_width=True)
    else:
        st.info("No patients found in the database. Go to 'Manage Patients' to add one.")

elif menu == "Manage Patients":
    st.header("Manage Patient Records")
    
    tab1, tab2 = st.tabs(["View Patients", "Add New Patient"])
    
    with tab1:
        patients = crud.get_all_patients()
        if patients:
            df = pd.DataFrame(patients)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No patient records found.")
            
    with tab2:
        st.subheader("Add a New Patient")
        with st.form("add_patient_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            p_id = col1.text_input("Patient ID (e.g., P004)")
            name = col2.text_input("Full Name")
            age = col1.number_input("Age", min_value=0, max_value=120, step=1)
            gender = col2.selectbox("Gender", ["Male", "Female", "Other"])
            location = col1.text_input("Location/City")
            contact = col2.text_input("Contact Number")
            
            # Fetch conditions to allow selection
            conditions_list = crud.get_all_conditions()
            condition_options = {c["ConditionName"]: c["ConditionID"] for c in conditions_list} if conditions_list else {}
            
            selected_conditions = st.multiselect(
                "Diagnosed Conditions", 
                options=list(condition_options.keys())
            )
            
            submitted = st.form_submit_button("Add Patient")
            
            if submitted:
                if p_id and name:
                    # Convert selected condition names back to IDs
                    cond_ids = [condition_options[c] for c in selected_conditions]
                    
                    new_patient = {
                        "PatientID": p_id,
                        "Name": name,
                        "Age": age,
                        "Gender": gender,
                        "Location": location,
                        "ContactNumber": contact,
                        "Conditions": cond_ids
                    }
                    try:
                        crud.create_patient(new_patient)
                        st.success(f"Patient {name} added successfully!")
                        st.rerun() # Refresh app to show new data
                    except Exception as e:
                        st.error(f"Error adding patient: {e}")
                else:
                    st.warning("Please fill out at least the Patient ID and Name.")

elif menu == "Manage Doctors":
    st.header("Manage Doctors")
    
    tab1, tab2 = st.tabs(["View Doctors", "Add New Doctor"])
    
    with tab1:
        doctors = crud.get_all_doctors()
        if doctors:
            df = pd.DataFrame(doctors)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No doctors found.")
            
    with tab2:
        st.subheader("Add a New Doctor")
        with st.form("add_doctor_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            d_id = col1.text_input("Doctor ID (e.g., D003)")
            name = col2.text_input("Full Name")
            spec = col1.text_input("Specialization")
            contact = col2.text_input("Contact Number")
            email = col1.text_input("Email")
            
            submitted = st.form_submit_button("Add Doctor")
            
            if submitted:
                if d_id and name:
                    new_doc = {
                        "DoctorID": d_id,
                        "Name": name,
                        "Specialization": spec,
                        "ContactNumber": contact,
                        "Email": email,
                        "AssignedPatients": []
                    }
                    crud.create_doctor(new_doc)
                    st.success(f"Doctor {name} added successfully!")
                    st.rerun()
                else:
                    st.warning("Please fill out at least Doctor ID and Name.")

elif menu == "Conditions":
    st.header("Chronic Conditions Reference")
    
    conditions = crud.get_all_conditions()
    
    if conditions:
        for c in conditions:
            with st.expander(f"{c.get('ConditionID', '')} - {c.get('ConditionName', 'Unknown')}"):
                st.write(f"**Description:** {c.get('Description', 'N/A')}")
                st.write(f"**Typical Symptoms:** {', '.join(c.get('TypicalSymptoms', []))}")
                st.write(f"**Standard Treatments:** {', '.join(c.get('StandardTreatments', []))}")
    else:
        st.info("No conditions tracked yet.")
