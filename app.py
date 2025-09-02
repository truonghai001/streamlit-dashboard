import streamlit as st
import pandas as pd

# page-wide customization
st.set_page_config(
    page_title="Iris Dashboard",
    page_icon="🌼",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# add selectbox
feature = st.selectbox(
    'Choose a feature to plot:',
    ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
)
st.line_chart(df[feature].head(sample_size))

# Add radio
species = st.radio(
    "Select species:",
    df['species'].unique()
)
filtered_df = df[df['species'] == species]
st.dataframe(filtered_df)

# add multi-select to choose multiple species
species_options = st.multiselect(
    "Select species:",
    df['species'].unique(),
    default=df['species'].unique()
)
filtered_df = df[df['species'].isin(species_options)]
st.data_editor(filtered_df)

# Organize interactive elements in a sidebar
with st.sidebar:
    st.header("Controls")
    sample_size = st.slider("Number of samples: ", 10, len(df), 20)
    feature = st.selectbox("Feature: ", df.columns[:-1])
    species = st.multiselect(
        "Species: ",
        df['species'].unique(),
        default=df['species'].unique()
    )
    
# Add Titles, Headers, Subheaders and Markdown
st.title("🌸 Iris Dataset Dashboard")
st.header("A quick tour of flower data analysis")
st.subheader("Visual Insights and Metrics")
st.markdown("Hand-crafted with Streamlit.")

# Layout - columns and containers for clean organization
col1, col2 = st.columns(2)
with col1:
    st.write("## Sepal Feature")
    st.line_chart(df[["sepal_length", "sepal_width"]])
with col2:
    st.write("## Petal Features")
    st.area_chart(df[["sepal_length", "sepal_width"]])
    
