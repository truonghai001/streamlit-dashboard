import streamlit as st
import pandas as pd

st.title('Hello, Streamlit Dashboard!')

# Load dataset
IRIS_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
COLUMN_NAMES = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
df = pd.read_csv(IRIS_URL, names=COLUMN_NAMES)

# View dataset
st.header("Step 1: Iris Dataset Loaded!")
st.write("Here is what the data look like:")
st.write(df.head())

# Shape & Structure
st.subheader("A quick look at dataset shape and structure")
st.write(f"Number of rows: {df.shape[0]}")
st.write(f"Number of columns: {df.shape[1]}")

# Data Types & Missing Values
st.subheader("Data Types and Null Values Info")
st.write(df.dtypes)
st.write(df.isnull().sum())

# Descriptive Statistics
st.subheader("Summary Statistics")
st.write(df.describe())

# Value Counts (Species Distribution)
st.subheader("Species Distribution in Iris Dataset")
st.write(df['species'].value_counts())

# expand/collaspe section - show full dataset
with st.expander("Show full dataset"):
    st.write(df)
    
# display data table with st.dataframe()
st.subheader("Iris Dataset Table View")
st.dataframe(df)

# Visualizing line chart
st.subheader("Linear Chart: Sepal Length and Width for First 20 Samples")
st.line_chart(df[['sepal_length', 'petal_length']].head(20))

# add a slider
sample_size = st.slider(
    "Select number of samples to display: ",
    min_value=10, max_value=len(df), value=20
)
st.line_chart(df[['sepal_length', 'sepal_width']].head(sample_size))
