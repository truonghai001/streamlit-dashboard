#https://medium.com/@nirbhaysingh281/stock-price-dashboard-app-in-streamlit-p-809d02b41073

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(page_title="Stock Dashboard", page_icon="📈")

st.title("📈 Stock Price Dashboard")
st.write("Enter a stock ticker symbol (e.g., **AAPL**, **GOOG**, **MSFT**, **TSLA**)")

# Input field
ticker = st.text_input("Stock Ticker Symbol:", "AAPL")

# Date range
start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date")

# Fetch data when user clicks button
if st.button("Get Stock Data"):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        if stock_data.empty:
            st.error("No data found for this ticker. Try another one.")
        else:
            st.success(f"Showing results for {ticker.upper()}")

            # Show data table
            st.subheader("📊 Data Preview")
            st.dataframe(stock_data.tail())

            # Plot closing price
            st.subheader("📉 Closing Price Chart")
            fig, ax = plt.subplots()
            stock_data["Close"].plot(ax=ax)
            ax.set_title(f"{ticker.upper()} Closing Price")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            st.pyplot(fig)
    except Exception as e:
        st.error(f"Error: {e}")