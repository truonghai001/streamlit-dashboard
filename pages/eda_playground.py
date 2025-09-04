"""
Build an EDA Playground with Streamlit
Reference: https://pub.towardsai.net/build-an-eda-playground-with-streamlit-403f4fc516ce
"""

import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
import io
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Data Prep Playground",
    layout="wide"
)

st.title("Data Prep Playground")
st.write("Upload your dataset, explore it, preprocess it, and visualize it interactively.")

# upload and review data
uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Preview")
    st.dataframe(df.head())
    
    st.subheader("Summary Statistics")
    st.write(df.describe(include="all"))
    
    st.subheader("Missing Values")
    st.write(df.isnull().sum())