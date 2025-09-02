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
