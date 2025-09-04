"""
Build a Data-Driven EV Dashboard with Streamlit and Python
https://medium.com/@_rohinim/build-a-data-driven-ev-dashboard-with-streamlit-and-python-1944016f6c75

"""


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import io

# Page configuration
st.set_page_config(
    page_title="Washington State EV Analysis",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Washington State theme
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #1abc9c 0%, #2ecc71 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1.2rem;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .subtitle {
        text-align: center;
        color: #34495e;
        font-size: 1.25rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }

    .data-source {
        background: linear-gradient(135deg, ##022e0c 0%, #a8e6cf 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #1abc9c;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    .metric-container {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        padding: 1.2rem;
        border-radius: 18px;
        color: #fff;
        text-align: center;
        margin: 0.7rem 0;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }

    .insight-box {
        background: linear-gradient(135deg,#022e0c 0%, #579e7e 100%);
        padding: 1.5rem;
        border-left: 5px solid #3498db;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.05);
    }

    .washington-green {
        color: #1abc9c;
        font-weight: bold;
    }
</style>

""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def load_washington_ev_data():
    """
    Load Washington State EV registration data from the official DOL dataset
    Dataset URL: https://data.wa.gov/api/views/f6w7-q2d2/rows.csv
    """
    try:
        # Official Washington State EV dataset
        url = "https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD"

        with st.spinner("Loading latest Washington State EV registration data..."):
            # Handle SSL issues by disabling certificate verification for this specific case
            import ssl
            import urllib.request

            # Create SSL context that doesn't verify certificates (for demo purposes)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            # Use requests with SSL verification disabled
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            response = requests.get(url, verify=False, timeout=30)
            df = pd.read_csv(io.StringIO(response.text))

        # Clean and standardize column names
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

        # Data cleaning and type conversion
        if 'Electric_Range' in df.columns:
            df['Electric_Range'] = pd.to_numeric(df['Electric_Range'], errors='coerce')
        if 'Model_Year' in df.columns:
            df['Model_Year'] = pd.to_numeric(df['Model_Year'], errors='coerce')
            # Filter out unreasonable years and NaN values
            df = df[(df['Model_Year'] >= 2010) & (df['Model_Year'] <= 2025)]
        if 'Base_MSRP' in df.columns:
            df['Base_MSRP'] = pd.to_numeric(df['Base_MSRP'], errors='coerce')
        elif 'MSRP' in df.columns:
            df['Base_MSRP'] = pd.to_numeric(df['MSRP'], errors='coerce')

        # Clean text columns - remove NaN and convert to string
        text_columns = ['Make', 'Model', 'County', 'City', 'Electric_Vehicle_Type']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).replace('nan', '')
                df = df[df[col] != '']  # Remove empty strings

        # Add calculated fields
        current_year = datetime.now().year
        if 'Model_Year' in df.columns:
            df['Vehicle_Age'] = current_year - df['Model_Year']

        st.success("Live data loaded successfully!")
        return df

    except Exception as e:
        st.warning(f"Could not load live data: {e}")
        st.info("🔄 Loading demo data that matches the real dataset structure...")
        return load_demo_data()


@st.cache_data
def load_demo_data():
    """
    Demo data that matches the structure of Washington State EV dataset
    """
    np.random.seed(42)
    n_records = 5000

    makes = ['TESLA', 'NISSAN', 'CHEVROLET', 'BMW', 'FORD', 'HYUNDAI', 'KIA', 'VOLKSWAGEN', 'AUDI', 'VOLVO']
    make_weights = [0.25, 0.15, 0.12, 0.08, 0.08, 0.07, 0.06, 0.05, 0.05, 0.09]

    models = {
        'TESLA': ['MODEL S', 'MODEL 3', 'MODEL X', 'MODEL Y'],
        'NISSAN': ['LEAF'],
        'CHEVROLET': ['BOLT EV', 'VOLT'],
        'BMW': ['I3', 'I4', 'IX'],
        'FORD': ['MUSTANG MACH-E', 'F-150 LIGHTNING'],
        'HYUNDAI': ['KONA ELECTRIC', 'IONIQ 5'],
        'KIA': ['NIRO EV', 'EV6'],
        'VOLKSWAGEN': ['ID.4'],
        'AUDI': ['E-TRON', 'E-TRON GT'],
        'VOLVO': ['XC40 RECHARGE', 'C40 RECHARGE']
    }

    cities = ['Seattle', 'Spokane', 'Tacoma', 'Vancouver', 'Bellevue', 'Kent', 'Everett',
              'Renton', 'Federal Way', 'Yakima', 'Bellingham', 'Kennewick', 'Auburn',
              'Pasco', 'Marysville', 'Lakewood', 'Redmond', 'Shoreline', 'Richland', 'Kirkland']

    counties = ['King', 'Pierce', 'Snohomish', 'Clark', 'Thurston', 'Kitsap', 'Whatcom',
                'Skagit', 'Cowlitz', 'Island', 'San Juan', 'Jefferson', 'Clallam']

    ev_types = ['Battery Electric Vehicle (BEV)', 'Plug-in Hybrid Electric Vehicle (PHEV)']

    data = []
    for i in range(n_records):
        make = np.random.choice(makes, p=make_weights)
        model = np.random.choice(models[make])
        ev_type = np.random.choice(ev_types, p=[0.75, 0.25])  # More BEVs than PHEVs
        year = np.random.choice(range(2012, 2025), p=np.array([0.02, 0.03, 0.04, 0.06, 0.08,
                                                               0.10, 0.12, 0.15, 0.15, 0.12,
                                                               0.08, 0.03, 0.02]))

        # Electric range based on vehicle type and year
        if ev_type == 'Battery Electric Vehicle (BEV)':
            if make == 'TESLA':
                base_range = np.random.choice([250, 300, 350, 400])
            elif year >= 2020:
                base_range = np.random.choice([150, 200, 250, 300])
            else:
                base_range = np.random.choice([80, 100, 150])
        else:  # PHEV
            base_range = np.random.choice([20, 25, 30, 35, 40])

        # MSRP estimation based on make, year, and type
        if make == 'TESLA':
            msrp = np.random.normal(60000, 20000)
        elif make in ['BMW', 'AUDI', 'VOLVO']:
            msrp = np.random.normal(50000, 15000)
        else:
            msrp = np.random.normal(35000, 10000)

        # Adjust for year
        msrp = msrp * (0.95 ** (2024 - year))  # Depreciation
        msrp = max(msrp, 15000)  # Minimum value

        data.append({
            'VIN_1_10': f'1N4AZ0CP{i:06d}',
            'County': np.random.choice(counties),
            'City': np.random.choice(cities),
            'State': 'WA',
            'Postal_Code': str(np.random.randint(98000, 99499)),
            'Model_Year': year,
            'Make': make,
            'Model': model,
            'Electric_Vehicle_Type': ev_type,
            'Clean_Alternative_Fuel_Vehicle_CAFV_Eligibility': np.random.choice([
                'Clean Alternative Fuel Vehicle Eligible',
                'Eligibility unknown as battery range has not been researched',
                'Not eligible due to low battery range'
            ], p=[0.6, 0.25, 0.15]),
            'Electric_Range': base_range,
            'Base_MSRP': int(msrp),
            'Legislative_District': str(np.random.randint(1, 50)),
            'DOL_Vehicle_ID': np.random.randint(100000000, 999999999),
            'Vehicle_Location': f"POINT ({-122 - np.random.random() * 2} {47 + np.random.random() * 2})",
            'Electric_Utility': np.random.choice(['PUGET SOUND ENERGY INC', 'SEATTLE CITY LIGHT',
                                                  'TACOMA POWER', 'SNOHOMISH COUNTY PUD']),
            '2020_Census_Tract': str(np.random.randint(53000000000, 53999999999))
        })

    return pd.DataFrame(data)


# Load the data
df = load_washington_ev_data()

# Header
st.markdown('<h1 class="main-header">Washington State EV Market Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Real-time insights from Washington DOL EV registration database</p>',
            unsafe_allow_html=True)

# Data source information
st.markdown("""
<div class="data-source">
    <h4>Data Source</h4>
    <p><strong>Washington State Department of Licensing (DOL)</strong></p>
    <p>This dashboard analyzes <strong>{:,} electric vehicle registrations</strong> from the official WA DOL database, 
    updated regularly and covering all Battery Electric Vehicles (BEVs) and Plug-in Hybrid Electric Vehicles (PHEVs) 
    currently registered in Washington State.</p>
</div>
""".format(len(df)), unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("🔧 Filters")
st.sidebar.markdown("*Filter the data to explore specific segments*")

# Year filter
if 'Model_Year' in df.columns:
    year_range = st.sidebar.slider(
        "Model Year Range",
        int(df['Model_Year'].min()),
        int(df['Model_Year'].max()),
        (int(df['Model_Year'].min()), int(df['Model_Year'].max()))
    )

# Make filter
if 'Make' in df.columns:
    # Clean and sort makes, removing NaN values
    make_options = [str(x) for x in df['Make'].dropna().unique() if str(x) != 'nan']
    make_options = sorted(make_options)

    # Get top 5 makes for default selection
    top_makes = df['Make'].value_counts().head(5).index.tolist()
    default_makes = [str(x) for x in top_makes if str(x) in make_options]

    selected_makes = st.sidebar.multiselect(
        "Vehicle Makes",
        options=make_options,
        default=default_makes[:5]  # Ensure we don't exceed available options
    )

# EV Type filter
if 'Electric_Vehicle_Type' in df.columns:
    # Clean EV types
    ev_type_options = [str(x) for x in df['Electric_Vehicle_Type'].dropna().unique() if str(x) != 'nan']

    ev_types = st.sidebar.multiselect(
        "Electric Vehicle Type",
        options=ev_type_options,
        default=ev_type_options
    )

# County filter
if 'County' in df.columns:
    # Clean and sort counties
    county_options = [str(x) for x in df['County'].dropna().unique() if str(x) != 'nan']
    county_options = sorted(county_options)

    # Default to major WA counties if they exist, otherwise first 3
    default_counties = []
    preferred_counties = ['King', 'Pierce', 'Snohomish']
    for county in preferred_counties:
        if county in county_options:
            default_counties.append(county)

    if not default_counties:  # If none of the preferred counties exist, take first 3
        default_counties = county_options[:3]

    selected_counties = st.sidebar.multiselect(
        "Counties",
        options=county_options,
        default=default_counties
    )

# Apply filters
filtered_df = df.copy()

if 'Model_Year' in df.columns:
    filtered_df = filtered_df[
        (filtered_df['Model_Year'] >= year_range[0]) &
        (filtered_df['Model_Year'] <= year_range[1])
        ]

if 'Make' in df.columns and selected_makes:
    # Convert to string for comparison to handle mixed types
    filtered_df = filtered_df[filtered_df['Make'].astype(str).isin(selected_makes)]

if 'Electric_Vehicle_Type' in df.columns and ev_types:
    filtered_df = filtered_df[filtered_df['Electric_Vehicle_Type'].astype(str).isin(ev_types)]

if 'County' in df.columns and selected_counties:
    filtered_df = filtered_df[filtered_df['County'].astype(str).isin(selected_counties)]

# Key Metrics
st.subheader("📈 Key Insights")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_evs = len(filtered_df)
    st.metric(
        label="Total EVs Registered",
        value=f"{total_evs:,}",
        delta=f"{(total_evs / len(df) * 100):.1f}% of dataset"
    )

with col2:
    if 'Electric_Vehicle_Type' in filtered_df.columns:
        bev_count = len(filtered_df[filtered_df['Electric_Vehicle_Type'].str.contains('BEV', na=False)])
        bev_pct = (bev_count / total_evs * 100) if total_evs > 0 else 0
        st.metric(
            label="Battery EVs (BEV)",
            value=f"{bev_count:,}",
            delta=f"{bev_pct:.1f}% of selection"
        )

with col3:
    if 'Electric_Range' in filtered_df.columns:
        avg_range = filtered_df['Electric_Range'].mean()
        st.metric(
            label="Average Range",
            value=f"{avg_range:.0f} miles",
            delta="EPA estimated range"
        )

with col4:
    if 'Model_Year' in filtered_df.columns and len(filtered_df) > 0:
        # Calculate average age, handling potential NaN values
        valid_years = filtered_df['Model_Year'].dropna()
        if len(valid_years) > 0:
            avg_age = datetime.now().year - valid_years.mean()
            st.metric(
                label="Fleet Average Age",
                value=f"{avg_age:.1f} years",
                delta="Getting newer!" if avg_age < 3 else "Maturing fleet"
            )
        else:
            st.metric(label="Fleet Average Age", value="N/A", delta="No data")
    else:
        st.metric(label="Fleet Average Age", value="N/A", delta="No data")

# Charts Row 1
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("EV Adoption Timeline")
    if 'Model_Year' in filtered_df.columns:
        yearly_registrations = filtered_df.groupby('Model_Year').size().reset_index()
        yearly_registrations.columns = ['Year', 'Registrations']

        fig_timeline = px.bar(
            yearly_registrations,
            x='Year',
            y='Registrations',
            title="EV Registrations by Model Year",
            color='Registrations',
            color_continuous_scale='Greens'
        )
        fig_timeline.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_timeline, use_container_width=True)

        # Insight
        growth_rate = (
                    (yearly_registrations['Registrations'].iloc[-1] - yearly_registrations['Registrations'].iloc[-5]) /
                    yearly_registrations['Registrations'].iloc[-5] * 100) if len(yearly_registrations) >= 5 else 0

        st.markdown(f"""
        <div class="insight-box">
            <strong>Insight:</strong> Washington's EV adoption shows <span class="washington-green">{growth_rate:.0f}% growth</span> 
            over recent years, 
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.subheader("Top EV Brands")
    if 'Make' in filtered_df.columns:
        make_counts = filtered_df['Make'].value_counts().head(8)

        fig_makes = px.pie(
            values=make_counts.values,
            names=make_counts.index,
            title="Market Share by Brand"
        )
        fig_makes.update_traces(textposition='inside', textinfo='percent+label')
        fig_makes.update_layout(height=400)
        st.plotly_chart(fig_makes, use_container_width=True)

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Geographic Distribution")
    if 'County' in filtered_df.columns:
        county_counts = filtered_df['County'].value_counts().head(10)

        fig_county = px.bar(
            x=county_counts.values,
            y=county_counts.index,
            orientation='h',
            title="EV Registrations by County",
            labels={'x': 'Number of EVs', 'y': 'County'}
        )
        fig_county.update_layout(height=400)
        st.plotly_chart(fig_county, use_container_width=True)

with col2:
    st.subheader("Range Analysis")
    if 'Electric_Range' in filtered_df.columns and 'Electric_Vehicle_Type' in filtered_df.columns:
        range_data = filtered_df[filtered_df['Electric_Range'] > 0]

        fig_range = px.box(
            range_data,
            x='Electric_Vehicle_Type',
            y='Electric_Range',
            title="Electric Range Distribution by Type"
        )
        fig_range.update_layout(height=400, xaxis_tickangle=45)
        st.plotly_chart(fig_range, use_container_width=True)

# Price Analysis (if MSRP data available)
if 'Base_MSRP' in filtered_df.columns:
    st.subheader("Price Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Price by make
        price_by_make = filtered_df.groupby('Make')['Base_MSRP'].mean().sort_values(ascending=False).head(10)

        fig_price = px.bar(
            x=price_by_make.values,
            y=price_by_make.index,
            orientation='h',
            title="Average MSRP by Brand",
            labels={'x': 'Average MSRP ($)', 'y': 'Make'}
        )
        fig_price.update_layout(height=400)
        st.plotly_chart(fig_price, use_container_width=True)

    with col2:
        # Price vs Range scatter
        if 'Electric_Range' in filtered_df.columns:
            price_range_data = filtered_df[(filtered_df['Base_MSRP'] > 0) & (filtered_df['Electric_Range'] > 0)]

            fig_scatter = px.scatter(
                price_range_data,
                x='Electric_Range',
                y='Base_MSRP',
                color='Make',
                title="Price vs Range Analysis",
                labels={'Electric_Range': 'EPA Range (miles)', 'Base_MSRP': 'MSRP ($)'}
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)

# Data Export Section
st.subheader("Export Filtered Data")
col1, col2, col3 = st.columns(3)

with col1:
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data (CSV)",
        data=csv,
        file_name=f"wa_ev_data_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col2:
    # Summary for Medium article
    summary_stats = pd.DataFrame({
        'Metric': ['Total Vehicles', 'Unique Makes', 'Unique Models', 'Counties Covered',
                   'Avg Electric Range', 'Most Popular Make', 'Most Popular County'],
        'Value': [
            f"{len(filtered_df):,}",
            f"{filtered_df['Make'].nunique() if 'Make' in filtered_df.columns else 'N/A'}",
            f"{filtered_df['Model'].nunique() if 'Model' in filtered_df.columns else 'N/A'}",
            f"{filtered_df['County'].nunique() if 'County' in filtered_df.columns else 'N/A'}",
            f"{filtered_df['Electric_Range'].mean():.0f} miles" if 'Electric_Range' in filtered_df.columns else 'N/A',
            f"{filtered_df['Make'].mode()[0] if 'Make' in filtered_df.columns and len(filtered_df) > 0 else 'N/A'}",
            f"{filtered_df['County'].mode()[0] if 'County' in filtered_df.columns and len(filtered_df) > 0 else 'N/A'}"
        ]
    })

    summary_csv = summary_stats.to_csv(index=False)
    st.download_button(
        label="Download Summary Stats",
        data=summary_csv,
        file_name=f"wa_ev_summary_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Raw Data View
with st.expander("View Raw Data"):
    st.dataframe(filtered_df.head(100), use_container_width=True)
    if len(filtered_df) > 100:
        st.info(f"Showing first 100 of {len(filtered_df):,} filtered records")



# Footer
st.markdown("---")
st.markdown(f"""
**Created by Rohini Mohan** | 
Data as of {datetime.now().strftime('%Y-%m-%d')} | 
Analyzing {len(filtered_df):,} of {len(df):,} total registrations |
 Powered by WA DOL Open Data
""")
