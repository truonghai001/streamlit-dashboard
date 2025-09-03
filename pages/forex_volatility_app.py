import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import requests_cache
from datetime import datetime, timedelta

# set up page configuration
st.set_page_config(
    page_title="FX Volatility Dashboard",
    page_icon="💱",
    layout="wide"
)

# initialize cache for API requests
requests_cache.install_cache('cache')

# API key
token = ""
