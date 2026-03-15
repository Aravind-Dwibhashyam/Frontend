Live Demo: 👉 [https://frontend-zxra8c5w4ip3f6k5gvjasp.streamlit.app/](https://frontend-zxra8c5w4ip3f6k5gvjasp.streamlit.app/)


15/3/2026
Streamlit (Python) — UI framework that turns Python scripts into interactive web apps. All forms, tables, and navigation are built with Streamlit widgets. Custom CSS is injected via st.markdown() for styling.
Backend
Python  — Application logic, ID generation, age calculation, and data wiring between form inputs and database documents all run in plain Python within the Streamlit script.
Database
MongoDB (via PyMongo) — NoSQL document store. Each ER entity maps to its own collection. Relationships (FK references) are maintained as string ID fields stored inside documents (e.g. patient_id, diagnosis_id, plan_id). No joins — data is fetched by querying on these reference fields.