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
with st.expander("World Happiness Dataset Table View"):
    st.dataframe(df_2023)
    
# Top and bottom 10 happiness countries (2023)
with st.expander("Top and bottom 10 happiness countries (2023)"):
    # compute top 10 and bottom 10 by happiness score
    top10 = df_2023.nlargest(10, "Ladder score").sort_values('Ladder score', ascending=True)
    bottom10 = df_2023.nsmallest(10, "Ladder score").sort_values('Ladder score', ascending=True)
    
    st.markdown("** Top 10 happiness countries **")
    fig_top = px.bar(
        top10,
        x='Ladder score', y='Country name',
        orientation='h',
        labels={"LLadder score": "Happiness Score", "Country name": "Country"}
    )
    st.plotly_chart(fig_top, use_container_width=True)
    
    st.markdown("** Bottom 10 happinest countries: **")
    fig_bottom = px.bar(
        bottom10,
        x='Ladder score', y='Country name',
        orientation='h',
        labels={"LLadder score": "Happiness Score", "Country name": "Country"}
    )
    st.plotly_chart(fig_bottom, use_container_width=True)
    
# add GDP vs. Happiness correlation
with st.expander("GDP vs. Happiness Correlation"):
    st.markdown("Scatter plot of **happiness score vs. GDP per capita** (Log Scate) for each country in 2023")
    fig_scatter = px.scatter(
        df_2023,
        x="Explained by: Log GDP per capita", y='Ladder score',
        hover_name="Country name",
        labels={"Life Ladder": "Happiness Score", "Log GDP per capita": "GDP per Capita (log)"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)