"""

"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
data = pd.read_csv("./ml_models/data/Summer_olympic_Medals.csv")
st.subheader("Hosted Country Impact on Olympic Medal Performance")

# filter by host country
host_country = st.selectbox(
    'Select Host Country',
    sorted(data['Host_Country'].unique())
)

# filder data for the selected host country
host_data = data[data['Host_Country'] == host_country]
country_data = data[data['Country_Name'] == host_country]

# extract years the country hosted the Olympucs
host_years = host_data['Year'].unique()

# Summarize medal counts for the host country
medal_counts = country_data.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().reset_index()
medal_counts['Total'] = medal_counts['Gold'] + medal_counts['Silver'] + medal_counts['Bronze']

# create a line chart to compare total medal counts
fig = px.line(
    medal_counts,
    x='Year', y='Total',
    labels={'Total': 'Total Medal Count'},
    title=f"Medal Performance of {host_country} over the years",
)
# update line color to gold and line width to 3 pixels
fig.update_traces(line=dict(color='#f5ce0a', width=4))

# Add annotations for host years
for year in host_years:
    fig.add_annotation(x=year, y=medal_counts[medal_counts['Year'] == year]['Total'].values[0],
                       text=f"Host Year ({year})", showarrow=True, arrowhead=2)
st.plotly_chart(fig)