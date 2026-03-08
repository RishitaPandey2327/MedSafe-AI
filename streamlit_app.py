"""
MedSafe AI - Main Streamlit Application
Front-end interface and main application logic
"""

import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract

from med_db import MedicineDatabase
from symptom import SymptomChecker
from ocr_utils import PrescriptionOCR
from risk_engine import RiskAssessment
from side_effects import SideEffectAnalyzer


# Page configuration
st.set_page_config(
    page_title="MedSafe AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Initialize components
@st.cache_resource
def init_components():
    """Initialize all application components"""

    med_db = MedicineDatabase()
    symptom_checker = SymptomChecker()
    ocr_processor = PrescriptionOCR()
    risk_assessor = RiskAssessment()
    side_effect_engine = SideEffectAnalyzer()

    return med_db, symptom_checker, ocr_processor, risk_assessor, side_effect_engine


def main():

    st.title("🏥 MedSafe AI - Intelligent Medicine Safety Assistant")
    st.markdown("---")

    # Initialize components
    med_db, symptom_checker, ocr_processor, risk_assessor, side_effect_engine = init_components()

    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")

        page = st.selectbox(
            "Select Service",
            [
                "🏠 Home",
                "💊 Medicine Interaction Checker",
                "🔍 Symptom & Doubt Solver",
                "📄 Prescription OCR",
                "⚠️ Side-Effect Monitor",
                "🚨 Emergency Risk Predictor"
            ]
        )

    # ---------------- HOME ----------------
    if page == "🏠 Home":

        st.header("Welcome to MedSafe AI")

        st.write(
        """
        MedSafe AI is your intelligent medical safety companion that helps you:

        • Check medicine interactions and safety  
        • Analyze symptoms and provide recommendations  
        • Extract prescription information using OCR  
        • Monitor medicine side effects  
        • Assess emergency health risks
        """
        )

    # ---------------- MEDICINE CHECKER ----------------
    elif page == "💊 Medicine Interaction Checker":

        st.header("💊 Medicine Interaction Checker")

        medicines = st.text_input("Enter medicines (comma separated):")

        if st.button("Check Interactions"):

            if medicines:

                med_list = [m.strip() for m in medicines.split(",")]

                interactions = med_db.check_interactions(med_list)

                st.success("Interaction Analysis Result")
                st.write(interactions)

    # ---------------- SYMPTOM ANALYSIS ----------------
    elif page == "🔍 Symptom & Doubt Solver":

        st.header("🔍 Symptom Interpretation")

        symptoms = st.text_area("Describe your symptoms")

        if st.button("Analyze Symptoms"):

            if symptoms:

                analysis = symptom_checker.analyze(symptoms)

                st.subheader("Detected Symptoms")
                st.write(analysis["symptoms_detected"])

                st.subheader("Possible Conditions")
                st.write(analysis["possible_conditions"])

                st.subheader("Recommendations")
                st.write(analysis["recommendations"])

                if analysis["seek_immediate_help"]:
                    st.error("⚠️ Seek Immediate Medical Help")

    # ---------------- PRESCRIPTION OCR ----------------
    elif page == "📄 Prescription OCR":

        st.header("📄 Prescription Scanner")

        uploaded_file = st.file_uploader(
            "Upload prescription image",
            type=['png', 'jpg', 'jpeg']
        )

        if uploaded_file is not None:

            image = Image.open(uploaded_file)

            st.image(image, caption="Uploaded Prescription", use_column_width=True)

            if st.button("Extract Text"):

                extracted_text = ocr_processor.extract_text(image)

                st.text_area(
                    "Extracted Text:",
                    extracted_text,
                    height=200
                )

    # ---------------- SIDE EFFECT MONITOR ----------------
    elif page == "⚠️ Side-Effect Monitor":

        st.header("⚠️ Side Effect Monitoring")

        col1, col2 = st.columns(2)

        with col1:
            medicine = st.text_input("Medicine Name")

        with col2:
            dosage = st.selectbox(
                "Dosage Level",
                ["low", "normal", "high"]
            )

        side_effects = st.text_input(
            "Experienced Side Effects (comma separated)"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        if st.button("Analyze Side Effects"):

            effects = [e.strip() for e in side_effects.split(",") if e]

            result = side_effect_engine.analyze(
                medicine,
                effects,
                age,
                gender,
                dosage
            )

            st.subheader("Side Effect Analysis Result")
            st.write(result)

    # ---------------- RISK PREDICTOR ----------------
    elif page == "🚨 Emergency Risk Predictor":

        st.header("🚨 Emergency Risk Predictor")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120
        )

        conditions = st.multiselect(
            "Existing Conditions",
            [
                "Diabetes",
                "Hypertension",
                "Heart Disease",
                "Asthma"
            ]
        )

        symptoms = st.text_input(
            "Current Symptoms (comma separated)"
        )

        if st.button("Assess Risk"):

            symptom_list = [s.strip() for s in symptoms.split(",") if s]

            risk_score = risk_assessor.calculate_risk(
                age,
                conditions,
                symptom_list
            )

            assessment = risk_assessor.assess_emergency(
                risk_score,
                symptom_list
            )

            st.metric("Risk Score", f"{risk_score}/100")

            st.subheader("Emergency Assessment")
            st.write(assessment)


if __name__ == "__main__":
    main()
