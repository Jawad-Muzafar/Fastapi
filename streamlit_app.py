from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import streamlit as st


DATA_FILE = Path(__file__).with_name("patient_data.json")


def load_patients() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)
    return data if isinstance(data, list) else []


def save_patients(patients: list[dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file_handle:
        json.dump(patients, file_handle, indent=2)


def normalize_diagnosis(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def normalize_patient(record: dict[str, Any]) -> dict[str, Any]:
    admission_date = record.get("admission_date")
    if isinstance(admission_date, date):
        admission_date = admission_date.isoformat()
    elif admission_date is None:
        admission_date = ""
    else:
        admission_date = str(admission_date)

    return {
        "id": record.get("id", ""),
        "name": record.get("name", ""),
        "age": record.get("age", ""),
        "gender": record.get("gender", ""),
        "diagnosis": normalize_diagnosis(record.get("diagnosis", "")),
        "admission_date": admission_date,
    }


def next_patient_id(patients: list[dict[str, Any]]) -> int:
    ids = [patient.get("id") for patient in patients if isinstance(patient.get("id"), int) and patient.get("id") > 0]
    return max(ids, default=0) + 1


def find_patient(patients: list[dict[str, Any]], patient_id: int) -> dict[str, Any] | None:
    for patient in patients:
        if patient.get("id") == patient_id:
            return patient
    return None


def app_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(12, 74, 110, 0.18), transparent 24%),
                    radial-gradient(circle at top right, rgba(45, 212, 191, 0.14), transparent 22%),
                    linear-gradient(180deg, #f8fbff 0%, #eef4f8 100%);
            }
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2.5rem;
                max-width: 1180px;
            }
            .hero {
                padding: 1.4rem 1.5rem;
                border-radius: 22px;
                background: rgba(255, 255, 255, 0.72);
                border: 1px solid rgba(15, 23, 42, 0.08);
                box-shadow: 0 14px 40px rgba(15, 23, 42, 0.08);
                backdrop-filter: blur(12px);
                margin-bottom: 1rem;
            }
            .hero h1 {
                margin-bottom: 0.2rem;
                color: #0f172a;
            }
            .hero p {
                margin: 0;
                color: #475569;
                font-size: 1.02rem;
            }
            .metric-card {
                padding: 1rem 1.1rem;
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.78);
                border: 1px solid rgba(15, 23, 42, 0.08);
                box-shadow: 0 10px 26px rgba(15, 23, 42, 0.06);
            }
            .soft-panel {
                padding: 1rem 1.1rem;
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.82);
                border: 1px solid rgba(15, 23, 42, 0.08);
                box-shadow: 0 10px 26px rgba(15, 23, 42, 0.05);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard(patients: list[dict[str, Any]]) -> None:
    normalized = [normalize_patient(patient) for patient in patients]
    total_patients = len(normalized)
    latest_id = max((patient["id"] for patient in normalized if isinstance(patient["id"], int)), default=0)
    latest_patient = next((patient for patient in reversed(normalized) if patient["id"]), None)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div>Total patients</div><h2>{total_patients}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div>Next patient ID</div><h2>{latest_id + 1}</h2></div>', unsafe_allow_html=True)
    with col3:
        last_label = latest_patient["name"] if latest_patient else "No records yet"
        st.markdown(f'<div class="metric-card"><div>Most recent record</div><h2>{last_label}</h2></div>', unsafe_allow_html=True)

    st.markdown("<div class='soft-panel'>", unsafe_allow_html=True)
    st.subheader("Patient Directory")
    if normalized:
        st.dataframe(normalized, use_container_width=True, hide_index=True)
    else:
        st.info("No patient records found. Use Add Patient to create the first one.")
    st.markdown("</div>", unsafe_allow_html=True)


def render_search(patients: list[dict[str, Any]]) -> None:
    st.subheader("Search Patient")
    patient_id = st.number_input("Patient ID", min_value=1, step=1, value=1)
    if st.button("Search", use_container_width=True):
        match = find_patient(patients, int(patient_id))
        if match:
            st.success("Patient found")
            st.json(normalize_patient(match))
        else:
            st.error("Patient not found")


def render_create_patient(patients: list[dict[str, Any]]) -> None:
    st.subheader("Add Patient")
    with st.form("create_patient_form", clear_on_submit=False):
        patient_name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=150, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        diagnosis = st.text_input("Diagnosis")
        admission_date = st.date_input("Admission date", value=date.today())
        submitted = st.form_submit_button("Save patient", use_container_width=True)

    if submitted:
        if not patient_name.strip() or not diagnosis.strip():
            st.error("Name and diagnosis are required.")
            return

        patient = {
            "id": next_patient_id(patients),
            "name": patient_name.strip(),
            "age": int(age),
            "gender": gender,
            "diagnosis": diagnosis.strip(),
            "admission_date": admission_date.isoformat(),
        }
        patients.append(patient)
        save_patients(patients)
        st.success(f"Patient {patient['name']} saved with ID {patient['id']}.")
        st.rerun()


def render_update_patient(patients: list[dict[str, Any]]) -> None:
    st.subheader("Update Patient")
    if not patients:
        st.info("No patients available to update.")
        return

    patient_id = st.number_input("Enter patient ID", min_value=1, step=1, value=1)
    if st.button("Load patient", use_container_width=True):
        st.session_state["update_patient_id"] = int(patient_id)

    selected_id = st.session_state.get("update_patient_id")
    if not selected_id:
        st.info("Enter an ID and load the patient details before editing.")
        return

    selected_patient = find_patient(patients, int(selected_id))
    if not selected_patient:
        st.error("Patient not found.")
        st.session_state.pop("update_patient_id", None)
        return

    normalized = normalize_patient(selected_patient)
    default_date = date.fromisoformat(normalized["admission_date"]) if normalized["admission_date"] else date.today()

    st.caption(f"Editing patient: {normalized['id']} - {normalized['name']}")
    with st.form("update_patient_form"):
        name = st.text_input("Name", value=normalized["name"])
        age = st.number_input("Age", min_value=1, max_value=150, step=1, value=int(normalized["age"]) if str(normalized["age"]).isdigit() else 1)
        gender = st.text_input("Gender", value=normalized["gender"])
        diagnosis = st.text_input("Diagnosis", value=normalized["diagnosis"])
        admission_date = st.date_input("Admission date", value=default_date)
        submitted = st.form_submit_button("Update patient", use_container_width=True)

    if submitted:
        selected_patient["name"] = name.strip()
        selected_patient["age"] = int(age)
        selected_patient["gender"] = gender.strip()
        selected_patient["diagnosis"] = diagnosis.strip()
        selected_patient["admission_date"] = admission_date.isoformat()
        save_patients(patients)
        st.success("Patient updated successfully.")
        st.rerun()


def render_delete_patient(patients: list[dict[str, Any]]) -> None:
    st.subheader("Delete Patient")
    if not patients:
        st.info("No patients available to delete.")
        return

    patient_id = st.number_input("Enter patient ID to delete", min_value=1, step=1, value=1, key="delete_patient_id")
    patient = find_patient(patients, int(patient_id))

    if patient:
        st.warning(f"This will delete patient {patient.get('id')} - {patient.get('name')}. This action cannot be undone.")
    else:
        st.info("No matching patient found yet.")

    if st.button("Delete patient", use_container_width=True):
        if not patient:
            st.error("Patient not found.")
            return

        patients.remove(patient)
        save_patients(patients)
        st.success("Patient deleted successfully.")
        st.rerun()


def main() -> None:
    st.set_page_config(page_title="Patient Records", page_icon="🏥", layout="wide")
    app_styles()

    st.markdown(
        """
        <div class="hero">
            <h1>Patient Records Manager</h1>
            <p>Deploy-ready Streamlit app for viewing, searching, creating, and updating patient records stored in JSON.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    patients = load_patients()

    page = st.sidebar.radio("Navigation", ["Dashboard", "Search", "Add Patient", "Update Patient", "Delete Patient"])
    st.sidebar.caption(f"Storage: {DATA_FILE.name}")

    if page == "Dashboard":
        render_dashboard(patients)
    elif page == "Search":
        render_search(patients)
    elif page == "Add Patient":
        render_create_patient(patients)
    elif page == "Update Patient":
        render_update_patient(patients)
    else:
        render_delete_patient(patients)


if __name__ == "__main__":
    main()