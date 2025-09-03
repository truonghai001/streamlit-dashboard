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
token = "xqABV8oDSI5HNDXU5ZQGACQy537wwXv8"


@st.cache_data(ttl=3600) # cache for 1 hour
def get_forex_pairs(included_currencies=None, use_included_currencies=True):
    url = 'https://financialmodelingprep.com/api/v3/symbol/available-forex-currency-pairs'
    querystring = {"apikey": token}
    
    try:
        response = requests.get(url, querystring)
        response.raise_for_status() # raise an exception for HTTP errors
        df = pd.DataFrame(response.json())
        
        # filter based on included currencies if the checkbox is checked
        if included_currencies and use_included_currencies:
            included_list = [curr.strip().upper() for curr in included_currencies.split(',') if curr.strip()]
            if included_list:
                filtered_df = pd.DataFrame()
                for pair in df['symbol']:
                    # extract the two currencies from the pair (e.g., ''EURUSD' -> 'EUR', 'USD')
                    if len(pair) >= 6:
                        curr1 = pair[:3]
                        curr2 = pair[3:6]
                        # check if both currencies are in the included list
                        if curr1 in included_list and curr2 in included_list:
                            filtered_df = pd.concat([filtered_df, df[df['symbol'] == pair]])
                df = filtered_df
        return df
    except Exception as e:
        st.error(f"Error fetching forex pairs: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=300) # cache for 5 minutes
def get_forex_quotes():
    url = 'https://financialmodelingprep.com/api/v3/quotes/forex'
    querystring = {"apikey": token}
    
    try:
        response = requests.get(url, querystring)
        response.raise_for_status()
        df = pd.DataFrame(response.json())
        return df
    except Exception as e:
        st.error(f"Error fetching forex quotes: {e}")
        return pd.DataFrame()
    

@st.cache_data(ttl=300) # cache for 5 mins
def get_historical_data(pair, timeframe):
    # map timeframe selection to API endpoint
    timeframe_map = {
        "15min": "15min",
        "1hour": "1hour",
        "4hours": "4hour",
        "1day": "1day",
        "1week": "1week"
    }
    
    api_timeframe = timeframe_map.get(timeframe, "1hour")
    
    # calculate date range (last 30 days)
    to_date = datetime.now().strftime('%Y-%m-%d')
    from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    url = f'https://financialmodelingprep.com/api/v3/historical-chart/{api_timeframe}/{pair}'
    querystring = {"apikey": token, "from": from_date, "to": to_date}
    
    try:
        response = requests.get(url, querystring)
        response.raise_for_status()
        df = pd.DataFrame(response.json())
        
        # convert date string to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # sort by date (ascending)
        df = df.sort_values('date')
        
        # calculate rolling volatility (standard deviation of returns)
        if len(df) > 0:
            df['return'] = df['close'].pct_change()
            df['volatility_20'] = df['return'].rolling(window=20).std() * 100 # convert to percentage
            
            # Calculate ATR (Average True Range)
            df['high_low'] = df['high'] - df['low']
            df['high_close'] = abs(df['high'] - df['close'].shift())
            df['low_close'] = abs(df['low'] - df['close'].shift())
            df['tr'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
            df['atr_14'] = df['tr'].rolling(window=14).mean()
        
        return df
    except Exception as e:
        st.error(f"Error fetching historical data: {e} for {pair} with {api_timeframe} timeframe")
        return pd.DataFrame()

def calculate_all_volatilities(pairs, timeframe):
    results = []
    
    for pair in pairs:
        try:
            df = get_historical_data(pair, timeframe)
            if len(df) > 0 and 'volatility_20' in df.columns:
                latest_volatility = df['volatility_20'].iloc[-1]
                results.append({
                    'pair': pair,
                    'volatility': latest_volatility
                })
        except Exception as e:
            st.warning(f"Could not calculate volatility for {pair}: {e}")
    
    return pd.DataFrame(results).sort_values('volatility', ascending=False)

def main():
    st.title("FX Volatility Dashboard")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Settings")
        
        # Currency filter inputs
        including_currencies = st.text_input("Including Currencies", value="USD,EUR,GBP,JPY,AUD,CAD,CHF,SGD,NZD,SEK,NOK,DKK",
                                           help="Enter currencies to include, separated by commas")
        use_included_currencies = st.checkbox("Use Including Currencies", value=True,
                                           help="When checked, only pairs with the currencies above will be shown. When unchecked, all pairs will be shown.")
        
        # Get forex pairs for dropdown
        forex_pairs_df = get_forex_pairs(included_currencies=including_currencies, 
                                        use_included_currencies=use_included_currencies)
        
        if not forex_pairs_df.empty:
            # Extract symbols for dropdown
            forex_symbols = forex_pairs_df['symbol'].tolist()
            selected_pair = st.selectbox("Select Forex Pair", forex_symbols, index=0)
        else:
            st.error("Could not load forex pairs")
            selected_pair = "EURUSD"  # Default
        
        # Timeframe selection
        timeframe_options = ["15min", "1hour", "4hours", "1day", "1week"]
        selected_timeframe = st.selectbox("Select Timeframe", timeframe_options, index=1)
        
        # Indicator selection
        indicator_options = ["20-period volatility", "14-period ATR"]
        selected_indicator = st.selectbox("Select Indicator", indicator_options, index=0)
        
        # Refresh button
        refresh = st.button("Refresh")
    
    # Main content area
    # Initialize last_refresh in session state if it doesn't exist
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    
    # Update last_refresh and clear cache if refresh button is clicked
    if refresh:
        st.session_state.last_refresh = datetime.now()
        # Clear cache to force data refresh
        get_forex_quotes.clear()
        get_historical_data.clear()
    
    # Get forex quotes - always execute this regardless of refresh button
    quotes_df = get_forex_quotes()
    
    # Display basic information for selected pair
    if not quotes_df.empty:
        selected_quote = quotes_df[quotes_df['symbol'] == selected_pair]
        
        if not selected_quote.empty:
            quote_data = selected_quote.iloc[0]
            
            # Display basic information with large font
            st.markdown(f"<h1 style='text-align: center;'>{selected_pair}: {quote_data['price']:.5f}</h1>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Change", f"{quote_data['change']:.5f}", f"{quote_data['changesPercentage']:.2f}%")
            with col2:
                st.metric("Day High", f"{quote_data['dayHigh']:.5f}")
            with col3:
                st.metric("Day Low", f"{quote_data['dayLow']:.5f}")
            with col4:
                st.metric("Year High", f"{quote_data['yearHigh']:.5f}")
        else:
            st.warning(f"No data available for {selected_pair}")
    
    # Get historical data and create chart
    historical_df = get_historical_data(selected_pair, selected_timeframe)
    
    if not historical_df.empty:
        # Create price chart with selected indicator
        fig = go.Figure()
        
        # Add price line
        fig.add_trace(go.Scatter(
            x=historical_df['date'],
            y=historical_df['close'],
            mode='lines',
            name='Close Price',
            line=dict(color='blue')
        ))
        
        # Add selected indicator on secondary y-axis
        if selected_indicator == "20-period volatility":
            fig.add_trace(go.Scatter(
                x=historical_df['date'],
                y=historical_df['volatility_20'],
                mode='lines',
                name='20-period Volatility (%)',
                line=dict(color='red'),
                yaxis='y2'
            ))
            secondary_axis_title = "Volatility (%)"
        else:  # "14-period ATR"
            fig.add_trace(go.Scatter(
                x=historical_df['date'],
                y=historical_df['atr_14'],
                mode='lines',
                name='14-period ATR',
                line=dict(color='green'),
                yaxis='y2'
            ))
            secondary_axis_title = "ATR"
        
        # Set up layout with dual y-axes
        fig.update_layout(
            title=f"{selected_pair} - {selected_timeframe} Chart with {selected_indicator}",
            xaxis_title="Date",
            yaxis_title="Price",
            yaxis2=dict(
                title=secondary_axis_title,
                overlaying="y",
                side="right"
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate and display volatility table for all pairs
        st.subheader("Forex Pairs Ranked by Volatility")
        
        with st.spinner("Calculating volatilities for filtered pairs..."):
            # Use the filtered forex_symbols list (respecting the "Including Currencies" filter)
            # Still limit to 10 pairs to avoid API rate limits
            volatility_df = calculate_all_volatilities(forex_symbols[:10], selected_timeframe)
            
            if not volatility_df.empty:
                st.dataframe(volatility_df, use_container_width=True)
            else:
                st.warning("Could not calculate volatilities")
    else:
        st.warning(f"No historical data available for {selected_pair} with {selected_timeframe} timeframe")

if __name__ == "__main__":
    main()