import streamlit as st
from logic import identify_medicine, check_interaction

st.set_page_config(page_title="MedSafe AI", layout="centered")
st.title("MedSafe AI - Interaction Module")

# Multi-select or text area for medicines
user_input = st.text_area("Enter medicines separated by commas (e.g., Paracetmol, Ibuprofan):")

if st.button("Check Safety"):
    if user_input:
        # Split input and clean up typos
        raw_names = [name.strip() for name in user_input.split(",")]
        identified_meds = []
        
        for name in raw_names:
            match = identify_medicine(name)
            if match:
                identified_meds.append(match)
        
        if identified_meds:
            st.success(f"Identified: {', '.join(identified_meds)}")
            
            # Get safety summaries
            results = check_interaction(identified_meds)
            st.subheader("Safety Summaries")
            for r in results:
                st.warning(r)
        else:
            st.error("No recognized medicines found. Please check the spelling.")