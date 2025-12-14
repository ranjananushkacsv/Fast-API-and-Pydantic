import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"  # Changed to localhost since you're running locally

st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox(
    "Occupation",
    ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
)

if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)
        
        if response.status_code == 200:
            result = response.json()
            
            # Check if response has the expected structure
            if "response" in result:
                prediction = result["response"]
                st.success(f"Predicted Insurance Premium Category: **{prediction['predicted_category']}**")
                
                if prediction["confidence"]:
                    st.write(f"🔍 Confidence: {prediction['confidence']:.2%}")
                
                if prediction["class_probabilities"]:
                    st.write("📊 Class Probabilities:")
                    for category, prob in prediction["class_probabilities"].items():
                        st.write(f"- {category}: {prob:.2%}")
            else:
                st.error(f"Unexpected response format: {result}")
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running on localhost:8000")
        st.info("Run this command in another terminal: `uvicorn app:app --reload`")