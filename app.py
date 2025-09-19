import streamlit as st
import pandas as pd
import joblib

# Load saved model
model = joblib.load('final_model.joblib')

st.title("🏠 House Price Predictor")

st.write("Enter the details of the house below:")

# User inputs
area = st.number_input("Area (sqft)", min_value=100, max_value=100000, value=1000)
bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=2)
bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=1)
mainroad = st.selectbox("Mainroad?", [0, 1])
basement = st.selectbox("Basement?", [0, 1])
parking = st.number_input("Parking", min_value=0, max_value=10, value=1)

# Collect inputs in DataFrame
input_df = pd.DataFrame([{
    'area': area,
    'bedrooms': bedrooms,
    'bathrooms': bathrooms,
    'mainroad': mainroad,
    'basement': basement,
    'parking': parking
}])

# Predict button
if st.button("Predict Price"):
    price = model.predict(input_df)[0]
    st.success(f"💰 Predicted House Price: ₹ {price:,.0f}")
