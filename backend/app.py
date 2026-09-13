
# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
sales_predictor_api = Flask("Product Store Sales Predictor")

# Load the trained machine learning model
model = joblib.load("SuperKart_model_v1_0.joblib")

# Define a route for the home page (GET request)
@sales_predictor_api.get('/')
def home():
    """
    Handles GET requests to the root URL ('/').
    Returns a simple welcome message.
    """
    return "Welcome to the Product Store Sales Prediction API!"

# Define an endpoint for single product prediction (POST request)
@sales_predictor_api.post('/v1/sales')
def predict_sales():
    """
    Handles POST requests to '/v1/sales'.
    Expects a JSON payload with product details and returns
    the predicted sales value as a JSON response.
    """
    try:
        product_data = request.get_json()

        # Extract relevant features from the JSON data
        sample = {
            'Product_Weight': product_data['Product_Weight'],
            'Product_Allocated_Area': product_data['Product_Allocated_Area'],
            'Product_MRP': product_data['Product_MRP'],
            'Store_Establishment_Year': product_data['Store_Establishment_Year'],
            'Product_Sugar_Content': product_data['Product_Sugar_Content'],
            'Product_Type': product_data['Product_Type'],
            'Store_Size': product_data['Store_Size'],
            'Store_Location_City_Type': product_data['Store_Location_City_Type'],
            'Store_Type': product_data['Store_Type']
        }

        # Convert to DataFrame
        input_df = pd.DataFrame([sample])

        # Predict sales
        predicted_sales = model.predict(input_df)[0]

        # Round to 2 decimals
        predicted_sales = round(float(predicted_sales), 2)

        return jsonify({'Predicted Product Store Sales Total': predicted_sales})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Define an endpoint for batch prediction (POST request)
@sales_predictor_api.post('/v1/salesbatch')
def predict_sales_batch():
    """
    Handles POST requests to '/v1/salesbatch'.
    Expects a CSV file with product details for multiple items
    and returns predicted sales values as a dictionary in JSON response.
    """
    try:
        file = request.files['file']
        input_df = pd.read_csv(file)

        predictions = model.predict(input_df).tolist()
        predictions = [round(float(p), 2) for p in predictions]

        ids = input_df['id'].tolist() if 'id' in input_df.columns else list(range(len(predictions)))
        output_dict = dict(zip(ids, predictions))

        return jsonify(output_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Run the Flask application in debug mode
if __name__ == '__main__':
  sales_predictor_api.run(host="0.0.0.0", port=7860, debug=True)

