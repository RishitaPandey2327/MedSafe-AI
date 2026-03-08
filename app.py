import streamlit as st
from logic import extract_medicines_from_image, check_interaction

# ... (Keep your title and manual input code)

st.divider()
st.subheader("📷 AI-Powered Prescription Scanner")
uploaded_file = st.file_uploader("Upload a clear image of your prescription", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    with st.spinner('AI is analyzing the prescription...'):
        structured_data, raw_text = extract_medicines_from_image(uploaded_file)
        
        if structured_data.get('medicines'):
            st.success("Detected Medicines & Active Salts")
            
            # Create a list of names for the interaction check
            med_names_to_check = []
            
            for med in structured_data['medicines']:
                # Professional display: Name -> Salt (Dosage)
                st.markdown(f"💊 **{med['name']}** → *{med['salt']}* ({med['dosage']})")
                med_names_to_check.append(med['name'])
            
            # Show safety warnings based on identified names
            results = check_interaction(med_names_to_check)
            if results:
                st.subheader("Safety Warnings")
                for r in results:
                    st.warning(r)
        else:
            st.info("The AI couldn't find any medicines in this image. Try a clearer photo.")