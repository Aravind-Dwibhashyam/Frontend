import streamlit as st
from pymongo import MongoClient
from datetime import datetime, date
import random
import string
from bson import ObjectId
import pandas as pd

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChronicCare · Patient Management",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f1923;
    border-right: 1px solid #1e3a4a;
}
section[data-testid="stSidebar"] * {
    color: #d0e8f2 !important;
}
section[data-testid="stSidebar"] .stRadio > label {
    color: #7ab8d4 !important;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Main title */
.main-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    color: #0f4c75;
    letter-spacing: -0.02em;
    margin-bottom: 0;
    line-height: 1.1;
}
.main-subtitle {
    color: #6b8fa3;
    font-size: 0.95rem;
    margin-top: 0.2rem;
    font-weight: 300;
    letter-spacing: 0.04em;
}

/* Section headers */
.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: #0f4c75;
    padding: 0.6rem 0 0.3rem 0;
    border-bottom: 2px solid #bbdefb;
    margin-bottom: 1rem;
}

/* Cards */
.patient-card {
    background: linear-gradient(135deg, #f0f7ff 0%, #e8f4fd 100%);
    border: 1px solid #c3dff5;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(15,76,117,0.06);
}
.metric-pill {
    display: inline-block;
    background: #0f4c75;
    color: white;
    border-radius: 20px;
    padding: 0.15rem 0.75rem;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 0.15rem;
}
.tag-pill {
    display: inline-block;
    background: #e3f2fd;
    color: #0f4c75;
    border: 1px solid #90caf9;
    border-radius: 20px;
    padding: 0.15rem 0.65rem;
    font-size: 0.75rem;
    margin: 0.1rem;
}
.status-active { color: #2e7d32; font-weight: 600; }
.status-inactive { color: #c62828; font-weight: 600; }

/* Buttons */
.stButton > button {
    background: #0f4c75;
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    letter-spacing: 0.03em;
    padding: 0.5rem 1.5rem;
    transition: background 0.2s;
}
.stButton > button:hover {
    background: #1565c0;
}

/* Expanders */
.streamlit-expanderHeader {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    color: #0f4c75;
}

/* Info boxes */
.stInfo { border-left-color: #0f4c75; }

/* Divider */
hr { border-color: #c3dff5; }

.success-box {
    background: #e8f5e9;
    border: 1px solid #a5d6a7;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #1b5e20;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)


# ─── MongoDB Connection ────────────────────────────────────────────────────────
@st.cache_resource
def get_db():
    client = MongoClient(st.secrets("MONGO_URI"))
    return client["chronic_care_db"]

db = get_db()


# ─── Helper: ID Generators ──────────────────────────────────────────────────────
def gen_id(prefix):
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{suffix}"


# ─── Sidebar Navigation ─────────────────────────────────────────────────────────
with st.sidebar:
    # Brand block
    st.markdown("""
    <div style='padding: 1.4rem 0.4rem 0.6rem 0.4rem;'>
        <div style='display:flex; align-items:center; gap:0.6rem;'>
            <span style='font-size:1.6rem; line-height:1;'>🩺</span>
            <div>
                <div style='font-family:"DM Serif Display",serif; font-size:1.25rem; color:#d0e8f2; line-height:1.1;'>ChronicCare</div>
                <div style='font-size:0.62rem; color:#4a7a94; letter-spacing:0.1em; text-transform:uppercase;'>Patient Management</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1px; background:#1e3a4a; margin: 0.5rem 0 1.2rem 0;'></div>", unsafe_allow_html=True)

    # Nav label
    st.markdown("<div style='font-size:0.62rem; color:#4a7a94; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.5rem; padding-left:0.2rem;'>Navigation</div>", unsafe_allow_html=True)

    page = st.radio(
        "",
        ["📋 Register Patient", "📊 View Patient Details", "📁 All Patients"],
        label_visibility="collapsed"
    )

    # Spacer then info card
    st.markdown("<div style='height:1px; background:#1e3a4a; margin: 1.4rem 0 1rem 0;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#0a1520; border:1px solid #1e3a4a; border-radius:8px; padding:0.8rem 1rem;'>
        <div style='font-size:0.62rem; color:#4a7a94; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.7rem;'>System Info</div>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;'>
            <span style='font-size:0.72rem; color:#4a7a94;'>Schema</span>
            <span style='font-size:0.72rem; color:#7ab8d4; font-weight:500; background:#0f2a3a; padding:0.1rem 0.5rem; border-radius:4px;'>ER v1.0</span>
        </div>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;'>
            <span style='font-size:0.72rem; color:#4a7a94;'>Database</span>
            <span style='font-size:0.72rem; color:#7ab8d4; font-weight:500; background:#0f2a3a; padding:0.1rem 0.5rem; border-radius:4px;'>MongoDB</span>
        </div>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <span style='font-size:0.72rem; color:#4a7a94;'>Collections</span>
            <span style='font-size:0.72rem; color:#7ab8d4; font-weight:500; background:#0f2a3a; padding:0.1rem 0.5rem; border-radius:4px;'>8</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: REGISTER PATIENT
# ══════════════════════════════════════════════════════════════════════════════
if page == "📋 Register Patient":
    st.markdown('<div class="main-title">Register New Patient</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Enter patient details across all modules — data is persisted to MongoDB with full relational schema.</div>', unsafe_allow_html=True)
    st.markdown("---")

    with st.form("patient_form", clear_on_submit=False):

        # ── SECTION 1: Patient Info ────────────────────────────────────────────
        st.markdown('<div class="section-header">👤 Patient Information</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            patient_name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma")
        with c2:
            dob = st.date_input("Date of Birth *", min_value=date(1900, 1, 1), max_value=date.today())
        with c3:
            gender = st.selectbox("Gender *", ["Male", "Female", "Other", "Prefer not to say"])

        # ── SECTION 2: Chronic Disease ─────────────────────────────────────────
        st.markdown('<div class="section-header">🧬 Chronic Disease</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            disease_name = st.text_input("Disease Name *", placeholder="e.g. Type 2 Diabetes")
            disease_type = st.selectbox("Disease Type", ["Metabolic", "Cardiovascular", "Respiratory", "Neurological", "Autoimmune", "Renal", "Other"])
        with c2:
            disease_desc = st.text_area("Description", placeholder="Brief description of the chronic condition...", height=100)

        # ── SECTION 3: Patient Diagnosis ────────────────────────────────────────
        st.markdown('<div class="section-header">🔬 Patient Diagnosis</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            date_diagnosed = st.date_input("Date Diagnosed *")
        with c2:
            severity_stage = st.selectbox("Severity Stage", ["Stage I – Mild", "Stage II – Moderate", "Stage III – Severe", "Stage IV – Critical"])
        with c3:
            doctor_id_diag = st.text_input("Doctor ID (FK)", placeholder="e.g. DOC-001", help="Doctor from Module-38")

        # ── SECTION 4: Clinical Metric ──────────────────────────────────────────
        st.markdown('<div class="section-header">📈 Clinical Metric</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_type = st.selectbox("Metric Type", ["Blood Glucose", "HbA1c", "Blood Pressure", "Cholesterol", "BMI", "SpO2", "Heart Rate", "Creatinine"])
        with c2:
            metric_value = st.number_input("Value", min_value=0.0, max_value=10000.0, step=0.1)
        with c3:
            metric_unit = st.text_input("Unit", placeholder="mg/dL, mmHg, %...")
        with c4:
            recorded_at = st.date_input("Recorded At", value=date.today())
        doctor_id_metric = st.text_input("Doctor ID for Metric (FK)", placeholder="e.g. DOC-001", key="metric_doc")

        # ── SECTION 5: Disease Episode ──────────────────────────────────────────
        st.markdown('<div class="section-header">📅 Disease Episode</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            ep_start = st.date_input("Episode Start Date")
            ep_end = None  # Left empty intentionally
        with c2:
            severity_level = st.selectbox("Severity Level", ["Low", "Moderate", "High", "Critical"])
            triggers = st.text_input("Triggers", placeholder="e.g. stress, diet, infection")
        with c3:
            doctor_id_ep = st.text_input("Doctor ID for Episode (FK)", placeholder="e.g. DOC-001", key="ep_doc")

        # ── SECTION 6: Risk Assessment ──────────────────────────────────────────
        st.markdown('<div class="section-header">⚠️ Risk Assessment</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            risk_score = st.slider("Risk Score", min_value=0, max_value=100, value=50, help="0 = No risk, 100 = Critical")
        with c2:
            risk_category = st.selectbox("Category", ["Low Risk", "Moderate Risk", "High Risk", "Very High Risk"])

        # ── SECTION 7: Treatment Plan ───────────────────────────────────────────
        st.markdown('<div class="section-header">💊 Treatment Plan</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            plan_goal = st.text_area("Treatment Goal", placeholder="e.g. Achieve HbA1c < 7% in 3 months", height=80)
        with c2:
            plan_start = st.date_input("Plan Start Date", value=date.today(), key="plan_start")
        with c3:
            doctor_id_plan = st.text_input("Doctor ID for Treatment (FK)", placeholder="e.g. DOC-001", key="plan_doc")

        # ── SECTION 8: Medication Adherence ─────────────────────────────────────
        st.markdown('<div class="section-header">💉 Medication Adherence</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            adh_log_date = st.date_input("Log Date", value=date.today(), key="adh_date")
        with c2:
            adh_status = st.selectbox("Adherence Status", ["Taken", "Missed", "Partial", "Skipped"])
        with c3:
            reason_skipped = st.text_input("Reason Skipped", placeholder="Leave blank if Taken")

        st.markdown("---")
        submit = st.form_submit_button("💾 Save Patient Record", use_container_width=True)

    # ── On Submit ────────────────────────────────────────────────────────────────
    if submit:
        if not patient_name:
            st.error("⚠️  Patient name is required.")
        else:
            # Calculate age
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            # Generate IDs
            patient_id  = gen_id("PAT")
            disease_id  = gen_id("DIS")
            diag_id     = gen_id("DGN")
            metric_id   = gen_id("MTR")
            episode_id  = gen_id("EPI")
            assess_id   = gen_id("RSK")
            plan_id     = gen_id("PLN")
            adherence_id = gen_id("ADH")

            doc_diag = doctor_id_diag or "DOC-000"
            doc_metric = doctor_id_metric or "DOC-000"
            doc_ep = doctor_id_ep or "DOC-000"
            doc_plan = doctor_id_plan or "DOC-000"

            # ── Build documents ──────────────────────────────────────────────────

            chronic_disease_doc = {
                "disease_id": disease_id,
                "name": disease_name,
                "type": disease_type,
                "description": disease_desc
            }

            patient_doc = {
                "patient_id": patient_id,
                "name": patient_name,
                "dob": str(dob),
                "age": age,
                "gender": gender
            }

            risk_assessment_doc = {
                "assessment_id": assess_id,
                "patient_id": patient_id,       # FK → Patient
                "risk_score": risk_score,
                "category": risk_category
            }

            patient_diagnosis_doc = {
                "diagnosis_id": diag_id,
                "patient_id": patient_id,        # FK → Patient
                "disease_id": disease_id,        # FK → Chronic Disease
                "assessment_id": assess_id,      # FK → Risk Assessment
                "date_diagnosed": str(date_diagnosed),
                "severity_stage": severity_stage,
                "current_status": "Active",      # hardcoded default
                "doctor_id": doc_diag
            }

            clinical_metric_doc = {
                "metric_id": metric_id,
                "diagnosis_id": diag_id,         # FK → Patient Diagnosis
                "metric_type": metric_type,
                "value": metric_value,
                "unit": metric_unit,
                "recorded_at": str(recorded_at),
                "doctor_id": doc_metric
            }

            disease_episode_doc = {
                "episode_id": episode_id,
                "diagnosis_id": diag_id,         # FK → Patient Diagnosis
                "start_date": str(ep_start),
                "end_date": None,
                "severity_levels": severity_level,
                "triggers": triggers,
                "doctor_id": doc_ep
            }

            treatment_plan_doc = {
                "plan_id": plan_id,
                "diagnosis_id": diag_id,         # FK → Patient Diagnosis
                "goal": plan_goal,
                "start_date": str(plan_start),
                "doctor_id": doc_plan
            }

            medication_adherence_doc = {
                "adherence_id": adherence_id,
                "plan_id": plan_id,              # FK → Treatment Plan
                "log_date": str(adh_log_date),
                "status": adh_status,
                "reason_skipped": reason_skipped if adh_status != "Taken" else ""
            }

            # ── Insert to MongoDB ───────────────────────────────────────────────
            try:
                db.chronic_diseases.insert_one(chronic_disease_doc)
                db.patients.insert_one(patient_doc)
                db.risk_assessments.insert_one(risk_assessment_doc)
                db.patient_diagnoses.insert_one(patient_diagnosis_doc)
                db.clinical_metrics.insert_one(clinical_metric_doc)
                db.disease_episodes.insert_one(disease_episode_doc)
                db.treatment_plans.insert_one(treatment_plan_doc)
                db.medication_adherences.insert_one(medication_adherence_doc)

                st.markdown(f"""
                <div class="success-box">
                ✅ &nbsp; Patient <strong>{patient_name}</strong> registered successfully!<br>
                <small>Patient ID: <code>{patient_id}</code> &nbsp;|&nbsp; Diagnosis ID: <code>{diag_id}</code> &nbsp;|&nbsp; Disease ID: <code>{disease_id}</code></small>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Database error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: VIEW PATIENT DETAILS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 View Patient Details":
    st.markdown('<div class="main-title">Patient Details</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Fetch and view complete patient records from MongoDB.</div>', unsafe_allow_html=True)
    st.markdown("---")

    search_col, btn_col = st.columns([3, 1])
    with search_col:
        search_input = st.text_input("Search by Patient Name or Patient ID", placeholder="e.g. Rahul or PAT-XY1234")
    with btn_col:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Search", use_container_width=True)

    if search_btn and search_input:
        query = {
            "$or": [
                {"name": {"$regex": search_input, "$options": "i"}},
                {"patient_id": {"$regex": search_input, "$options": "i"}}
            ]
        }
        patients = list(db.patients.find(query))

        if not patients:
            st.warning("No patients found matching your search.")
        else:
            for pat in patients:
                pid = pat["patient_id"]
                st.markdown(f"""
                <div class="patient-card">
                    <b style="font-size:1.1rem;color:#0f4c75;">{pat.get('name','N/A')}</b>
                    &nbsp;<span class="tag-pill">ID: {pid}</span>
                    &nbsp;<span class="tag-pill">{pat.get('gender','')}</span>
                    &nbsp;<span class="tag-pill">Age: {pat.get('age','')}</span>
                    &nbsp;<span class="tag-pill">DOB: {pat.get('dob','')}</span>
                </div>
                """, unsafe_allow_html=True)

                # Diagnosis
                diag = db.patient_diagnoses.find_one({"patient_id": pid})
                if diag:
                    with st.expander("🔬 Diagnosis Details"):
                        d1, d2, d3 = st.columns(3)
                        d1.metric("Diagnosis ID", diag.get("diagnosis_id","—"))
                        d2.metric("Date Diagnosed", diag.get("date_diagnosed","—"))
                        d3.metric("Severity Stage", diag.get("severity_stage","—"))
                        d1.metric("Current Status", diag.get("current_status","—"))
                        d2.metric("Doctor ID", diag.get("doctor_id","—"))

                    # Chronic Disease
                    dis = db.chronic_diseases.find_one({"disease_id": diag.get("disease_id")})
                    if dis:
                        with st.expander("🧬 Chronic Disease"):
                            st.write(f"**Name:** {dis.get('name','—')} &nbsp;|&nbsp; **Type:** {dis.get('type','—')}")
                            st.write(f"**Description:** {dis.get('description','—')}")

                    # Clinical Metric
                    metric = db.clinical_metrics.find_one({"diagnosis_id": diag.get("diagnosis_id")})
                    if metric:
                        with st.expander("📈 Clinical Metric"):
                            m1, m2, m3, m4 = st.columns(4)
                            m1.metric("Type", metric.get("metric_type","—"))
                            m2.metric("Value", f"{metric.get('value','—')} {metric.get('unit','')}")
                            m3.metric("Recorded At", metric.get("recorded_at","—"))
                            m4.metric("Doctor ID", metric.get("doctor_id","—"))

                    # Disease Episode
                    ep = db.disease_episodes.find_one({"diagnosis_id": diag.get("diagnosis_id")})
                    if ep:
                        with st.expander("📅 Disease Episode"):
                            e1, e2, e3, e4 = st.columns(4)
                            e1.metric("Episode ID", ep.get("episode_id","—"))
                            e2.metric("Start Date", ep.get("start_date","—"))
                            e3.metric("End Date", ep.get("end_date","—"))
                            e4.metric("Severity", ep.get("severity_levels","—"))
                            st.write(f"**Triggers:** {ep.get('triggers','—')}")

                    # Treatment Plan
                    plan = db.treatment_plans.find_one({"diagnosis_id": diag.get("diagnosis_id")})
                    if plan:
                        with st.expander("💊 Treatment Plan"):
                            p1, p2, p3 = st.columns(3)
                            p1.metric("Plan ID", plan.get("plan_id","—"))
                            p2.metric("Start Date", plan.get("start_date","—"))
                            p3.metric("Doctor ID", plan.get("doctor_id","—"))
                            st.write(f"**Goal:** {plan.get('goal','—')}")

                            # Medication Adherence
                            adh = db.medication_adherences.find_one({"plan_id": plan.get("plan_id")})
                            if adh:
                                with st.expander("💉 Medication Adherence"):
                                    a1, a2, a3 = st.columns(3)
                                    a1.metric("Log Date", adh.get("log_date","—"))
                                    status_val = adh.get("status","—")
                                    a2.metric("Status", status_val)
                                    a3.metric("Reason Skipped", adh.get("reason_skipped","—") or "N/A")

                # Risk Assessment
                risk = db.risk_assessments.find_one({"patient_id": pid})
                if risk:
                    with st.expander("⚠️ Risk Assessment"):
                        r1, r2, r3 = st.columns(3)
                        r1.metric("Assessment ID", risk.get("assessment_id","—"))
                        r2.metric("Risk Score", risk.get("risk_score","—"))
                        r3.metric("Category", risk.get("category","—"))

                st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: ALL PATIENTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📁 All Patients":
    st.markdown('<div class="main-title">All Patients</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Overview of all registered patients in the database.</div>', unsafe_allow_html=True)
    st.markdown("---")

    patients = list(db.patients.find({}, {"_id": 0}))
    if not patients:
        st.info("No patients registered yet. Go to **Register Patient** to add one.")
    else:
        # Summary metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Patients", len(patients))
        m2.metric("Collections Active", 8)
        m3.metric("Database", "MongoDB · chronic_care_db")

        st.markdown("---")

        # Table
        df = pd.DataFrame(patients)[["patient_id", "name", "age", "gender", "dob"]]
        df.columns = ["Patient ID", "Name", "Age", "Gender", "Date of Birth"]
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Quick lookup from table
        st.markdown("### 🔎 Quick Lookup")
        sel_pid = st.selectbox("Select Patient ID to view summary", [p["patient_id"] for p in patients])
        if sel_pid:
            pat = db.patients.find_one({"patient_id": sel_pid})
            diag = db.patient_diagnoses.find_one({"patient_id": sel_pid})
            risk = db.risk_assessments.find_one({"patient_id": sel_pid})

            col1, col2, col3 = st.columns(3)
            col1.info(f"**Name:** {pat.get('name')}\n\n**Gender:** {pat.get('gender')}\n\n**Age:** {pat.get('age')}")
            if diag:
                col2.info(f"**Diagnosis ID:** {diag.get('diagnosis_id')}\n\n**Status:** {diag.get('current_status')}\n\n**Severity:** {diag.get('severity_stage')}")
            if risk:
                col3.info(f"**Risk Score:** {risk.get('risk_score')}\n\n**Category:** {risk.get('category')}")