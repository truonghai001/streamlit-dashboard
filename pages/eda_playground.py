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
    
# processing option
# creating slidebar
st.sidebar.header("Preprocessing Options")
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

code_snippets = []

# categorical columns
if categorical_cols: st.sidebar.subheader("Encode Categorical")
encoding_method = st.sidebar.selectbox("Encoding", ["None", "Label Encoding", "One-Hot Encoding"])
if encoding_method == "Label Encoding":
    le = LabelEncoder()
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col].astype(str))
    code_snippets.append("# Label Encoding categorical columns\n...")
elif encoding_method == "One-Hot Encoding":
    df = pd.get_dummies(df, columns=categorical_cols)
    code_snippets.append("# One-Hot Encoding categorical columns\n...")

#Numerical columns
if numerical_cols:
    st.sidebar.subheader("Scale Numerical")
    scaling_method = st.sidebar.selectbox("Scaling", ["None", "StandardScaler", "MinMaxScaler"])
    if scaling_method == "StandardScaler":
        scaler = StandardScaler()
        df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
        code_snippets.append("# Standard Scaling numerical columns\n...")
    elif scaling_method == "MinMaxScaler":
        scaler = MinMaxScaler()
        df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
        code_snippets.append("# MinMax Scaling numerical columns\n...")
        
st.subheader("Processed Data")
st.dataframe(df.head())
