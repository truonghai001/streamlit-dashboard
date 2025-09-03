import streamlit as st
import pandas as pd
import numpy as np
import pickle
import base64
import seaborn as sns
import matplotlib.pyplot as plt

st.write("""

# Churn Prediction App

Customer churn is defined as the loss of customers after a certain period of time. Companies are interested in targeting customers

who are likely to churn. They can target these customers with special deals and promotions to influence them to stay with

the company. 

This app predicts the probability of a customer churning using Telco Customer data. Here

customer churn means the customer does not make another purchase after a period of time. 

""")


df_selected = pd.read_csv('./ml_models/data/telco_churn.csv')
df_selected_all = df_selected[['gender', 'Partner', 'Dependents', 'PhoneService','tenure', 'MonthlyCharges', 'target']].copy()

st.dataframe(df_selected)

