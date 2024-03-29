# -*- coding: utf-8 -*-
"""Streamlit Data Science.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mrKrABap7s0bFjrg9KVSSs9_JszYZa61
"""

#!pip install xgboost

import streamlit as st
import numpy as np
import pandas as pd
import pickle
from xgboost import XGBRegressor

load_model = pickle.load(open('pld_estate_prediction_model.pkl', 'rb'))

def predict_price(apartment_type, square_meters, construction_year,
                  floor_number, district, construction_type,
                  floor, level_of_completion):

    # Prepare input features as a DataFrame
    input_data = x = np.zeros(len(features.columns))

    district_index = np.where(features.columns == district)[0][0]
    costruction_type_index = np.where(features.columns == construction_type)[0][0]
    floor_index = np.where(features.columns == floor)[0][0]
    completion_index = np.where(features.columns == level_of_completion)[0][0]

    input_data[0] = apartment_type_dict[apartment_type]
    input_data[1] = square_meters
    input_data[2] = construction_year
    input_data[3] = floor_number
    input_data[district_index] = 1
    input_data[costruction_type_index] = 1
    input_data[floor_index] = 1
    input_data[completion_index] = 1


    # Make prediction
    prediction = load_model.predict([input_data])[0]

    return prediction
apartment_type_dict = {'One room apartment': 1,
                         'Studio': 2,
                         'Two-room apartment': 3,
                         'Three-room apartment': 4,
                         'Маisonette': 5,
                         'Multi-room apartment': 6}

features_cols = ['apartment type', 'square meters', 'construction year', 'floor number',
       'Belomorski', 'Central', 'Gagarin', 'Hristo Smirnenski', 'Judicial',
       'Kamenitza 1', 'Kamenitza 2', 'Komatevo', 'Kurshiyaka', 'Marasha',
       'Ostromila', 'Proslav', 'Southern', 'Sunrise', 'Thrace', 'Western',
       'Youth hill', ' Panel', 'Bricks', 'Formwork', 'Joist', 'Attic',
       'Basement', 'First', 'Ground floor', 'Last', 'Not last', 'Unknown',
       'In a project', 'In construction', 'Not specified']

features = pd.DataFrame(columns = features_cols)

# Streamlit UI
st.header("Plovdiv Apartments")
st.header("Price Prediction App", divider="gray")

st.text("\nThe model for this app was trained on real estate data for apartments only from www.alo.bg"
        "\nIn order to make a prediction you need to input 8 parameters\n"
        "(the values of the numeric parameters should be inclusively\nbetween the min/max values showed in brackets):\n"
        "\n-Square meters (min:10, max=200)\n-Construction year (min: 1886, max=2027)"
        "\n-Floor number (min=1, max=19)\n-Apartment type\n-District\n-Construction type\n-Floor type\n-Level of completion")

# Input for numerical features

square_meters = st.number_input("Enter Square meters:", min_value=10, max_value=600)
construction_year = st.number_input("Enter Construction year:", min_value=1886, max_value=2027)
floor_number = st.number_input("Enter Floor number:", min_value=1, max_value=19)

# Dropdowns for categorical features

apartment_type = st.selectbox('Select Apartment type:', np.array(list(apartment_type_dict.keys())))
district = st.selectbox('Select District:', features.columns[4:21].values)
construction_type = st.selectbox('Select Construction type:', features.columns[21:25].values)
floor = st.selectbox('Select Floor type:', features.columns[25:32].values)
level_of_completion = st.selectbox('Select Level of completion:', features.columns[32:].values)


if st.button("Predict Price"):
    predicted_price = predict_price(apartment_type, square_meters, construction_year,
                                    floor_number, district, construction_type, floor, level_of_completion)

    st.success(f"Predicted Price: €{predicted_price:,.2f}")

st.text("The Root Mean Squared Error on the test set is €11,828."
       "\nHowever there might be big predictive deviations due to the nature of the scraped data."
       "\nThe real estate data doesn't contain parameters like furnishing, number of bathrooms,"
       "\nunit type(e.g. residential building, house or hotel apartment, etc.)"
       "\nAlso, there are only 'In project' and 'In construction' level of completion types"
       "\nso we have to mark all other buildings with completion type 'Not specified'"
       "\nwhich adds further to the model's error."
       "\nThese are some of the few factors that affect the app's performance"
       "\nbut regardless, you can get a very good price estimate of an apartment in Plovdiv.")
