import streamlit as st
import pandas as pd
import plotly.express as px


# set up page configuration
st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="💱",
    layout="wide"
)

# https://medium.com/data-storytelling-corner/insanely-simple-streamlit-expanders-for-better-data-storytelling-f4d25d98002d
DATA_FILE_URL = "https://raw.githubusercontent.com/loewenj700/global_happiness/refs/heads/main/WHR2024.csv"

# load the world happiness data (all years and filter for 2023)
df = pd.read_csv(DATA_FILE_URL)
df_2023 = df[df['Year'] == 2023]

# display data table with st.dataframe()
st.subheader("World Happiness Dataset Table View")
st.dataframe(df_2023)