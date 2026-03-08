"""
Main Integration Entry for MedSafe AI
"""

import streamlit as st
from symptom import SymptomChecker
from risk_engine import RiskAssessment
from side_effects import SideEffectAnalyzer
from ai_explainer import AIExplainer
from utils import setup_logger, log_event


def main():

    setup_logger()

    st.title("MedSafe AI Health Assistant")

    symptom_checker = SymptomChecker()
    risk_engine = RiskAssessment()
    side_effect_engine = SideEffectAnalyzer()
    ai_explainer = AIExplainer()

    st.header("User Information")

    age = st.number_input("Age", 1, 120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    medicine = st.text_input("Medicine Name")
    dosage = st.selectbox("Dosage Level", ["low", "normal", "high"])

    symptoms = st.text_area("Describe your symptoms")

    side_effects = st.text_input(
        "Side effects experienced (comma separated)"
    )

    if st.button("Analyze Health"):

        log_event("Analysis started")

        symptom_result = symptom_checker.analyze(symptoms)

        side_effect_list = [s.strip() for s in side_effects.split(",") if s]

        side_effect_result = side_effect_engine.analyze(
            medicine,
            side_effect_list,
            age,
            gender,
            dosage
        )

        risk_score = risk_engine.calculate_risk(
            age,
            symptoms=symptom_result["symptoms_detected"],
            medications=[medicine]
        )

        risk_assessment = risk_engine.assess_emergency(
            risk_score,
            symptom_result["symptoms_detected"]
        )

        ai_help = ai_explainer.generate_explanation(symptom_result)

        st.subheader("Symptom Analysis")
        st.write(symptom_result)

        st.subheader("Side Effect Analysis")
        st.write(side_effect_result)

        st.subheader("Risk Score")
        st.metric("Risk Score", risk_score)

        st.subheader("Emergency Assessment")
        st.write(risk_assessment)

        st.subheader("Educational Explanation")
        st.write(ai_help)


if __name__ == "__main__":
    main()
