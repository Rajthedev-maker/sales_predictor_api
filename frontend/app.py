
import streamlit as st
import pandas as pd
import numpy as np
import requests
import os

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Prediction App")
st.write("This tool predicts the Sales of Superkart Company based on the products details.")

st.subheader("Enter the listing details:")

# Collect user input
Product_Weight = st.number_input("Weight of each product", min_value=0)
Product_Allocated_Area = st.number_input("Ratio of the allocated display area of each product to the total display area of all the products in a store", min_value=0)
Product_MRP = st.number_input("Maximum retail price of each product", min_value=0)
Store_Establishment_Year = st.number_input("Year in which the store was established", min_value=1800, value=2000)

Product_Sugar_Content = st.selectbox("Sugar content of each product", ["Low Sugar", "Regular", "No Sugar"])
Product_Type = st.selectbox("Product category", [
    "Fruits and Vegetables", "Snack Foods", "Frozen Foods", "Dairy", "Household", "Baking Goods", "Canned",
    "Health and Hygiene", "Meat", "Soft Drinks", "Breads", "Hard Drinks", "Starchy Foods", "Breakfast",
    "Seafood", "Others"
])
Store_Size = st.selectbox("Store size", ["Medium", "High", "Small"])
Store_Location_City_Type = st.selectbox("City type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])

# Build payload
input_data = {
    'Product_Weight': Product_Weight,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_MRP': Product_MRP,
    'Store_Establishment_Year': Store_Establishment_Year,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Type': Product_Type,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type
}

# Predict button
if st.button("Predict", type="primary"):
    #response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data)
    if response.status_code == 200:
        prediction = response.json()['Predicted Product Store Sales Total']
        st.success(f"The predicted Total revenue generated is: {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

st.subheader("Batch Prediction")

uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
