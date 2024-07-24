#streamlit run ARTI404-Project/stock4.py 

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Initialize session state
if 'last_10_stocks' not in st.session_state:
    st.session_state['last_10_stocks'] = []

if 'interval_options' not in st.session_state:
    st.session_state['interval_options'] = []

# Function to fetch live stock data
def fetch_stock_data(ticker, period, interval):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    return hist

# Function to fetch additional stock info
def fetch_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return info

# Function to update last 10 stocks
def update_last_10_stocks(ticker):
    if ticker not in st.session_state['last_10_stocks']:
        st.session_state['last_10_stocks'].append(ticker)
        if len(st.session_state['last_10_stocks']) > 10:
            st.session_state['last_10_stocks'].pop(0)

def check_ticker(ticker, period, interval):
    check = fetch_stock_data(ticker, period, interval)
    if not check.empty:
        update_last_10_stocks(ticker)
        st.sidebar.success(f"Data for {ticker} has been loaded.")
        return True
    else:
        st.sidebar.error("No data found for the given ticker")
        return False

# Sidebar
st.sidebar.image("ARTI404-Project/stock_logo.png", caption="Stock Logo")

st.sidebar.title("Last 10 Stocks")
selected_sidebar_stock = st.sidebar.radio("Select a stock:", st.session_state['last_10_stocks'], index=0 if st.session_state['last_10_stocks'] else None)

st.sidebar.title("Stock Selection")
# Market selection in the sidebar
market = st.sidebar.selectbox("Select market:", ["US", "Canada", "UK", "Germany", "France", "Japan", "Australia"], index=0)

# Define valid intervals for each period
interval_options = {
    '1d': ['1m', '2m', '5m', '15m', '30m', '60m', '90m'],
    '5d': ['5m', '15m', '30m', '60m', '90m', '1d'],
    '1mo': ['15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk'],
    '3mo': ['1d', '5d', '1wk', '1mo'],
    '6mo': ['1d', '5d', '1wk', '1mo', '3mo'],
    '1y': ['1h', '1d', '5d', '1wk', '1mo', '3mo'],
    '2y': ['1d', '5d', '1wk', '1mo', '3mo'],
    '5y': ['1d', '5d', '1wk', '1mo', '3mo'],
    '10y': ['1wk', '1mo', '3mo'],
    'ytd': ['1d', '5d', '1wk', '1mo'],
    'max': ['1wk', '1mo', '3mo']
}

# Function to update interval options based on selected period
def update_interval_options(period):
    st.session_state['interval_options'] = interval_options.get(period, [])

# Period selection in the sidebar
period = st.sidebar.selectbox("Select period:", list(interval_options.keys()), index=1, on_change=update_interval_options, args=(st.session_state.get('period', '1d'),))

# Update interval options based on initial period
if not st.session_state['interval_options']:
    update_interval_options(period)

# Interval selection in the sidebar
interval = st.sidebar.selectbox("Select interval:", st.session_state['interval_options'], index=0)

ticker_input = st.sidebar.text_input("Enter stock ticker (e.g., AAPL, GOOGL, MSFT):", value="").strip().upper()

# Map market selection to appropriate suffix
market_suffix = {
    "US": "",
    "Canada": ".TO",
    "UK": ".L",
    "Germany": ".DE",
    "France": ".PA",
    "Japan": ".T",
    "Australia": ".AX"
}

def format_ticker(ticker, market):
    if market == "Canada" and ticker_input.endswith(".V"):
        return ticker + ".V"
    return ticker + market_suffix[market]

# Main page
st.title("Live Stock Market Data")

def display_stock_data(ticker, period, interval):
    data = fetch_stock_data(ticker, period, interval)
    if not data.empty:
        update_last_10_stocks(ticker)
        st.sidebar.success(f"Data for {ticker} has been loaded.")

        # Fetch additional stock info
        info = fetch_stock_info(ticker)
        
        # Display header with current stock information
        st.header(f"{ticker} ({info.get('shortName', 'N/A')})")
        st.subheader("Current Information")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Market Price:** {info.get('regularMarketPrice', 'N/A')}")
            st.write(f"**Market Change:** {info.get('regularMarketChange', 'N/A')}")
            st.write(f"**Open:** {info.get('open', 'N/A')}")
            st.write(f"**Day's Range:** {info.get('dayHigh', 'N/A')} - {info.get('dayLow', 'N/A')}")
        with col2:
            st.write(f"**Volume:** {info.get('volume', 'N/A')}")
            st.write(f"**Avg. Volume:** {info.get('averageVolume', 'N/A')}")
            st.write(f"**Previous Close:** {info.get('previousClose', 'N/A')}")
            st.write(f"**52 Week Range:** {info.get('fiftyTwoWeekHigh', 'N/A')} - {info.get('fiftyTwoWeekLow', 'N/A')}")
        with col3:
            st.write(f"**Bid:** {info.get('bid', 'N/A')}")
            st.write(f"**Ask:** {info.get('ask', 'N/A')}")

        # Fetch and display additional stock info
        st.subheader("Additional Information")
        
        col4, col5 = st.columns(2)
        with col4:
            st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
            st.write(f"**Beta (5Y Monthly):** {info.get('beta', 'N/A')}")
            st.write(f"**PE Ratio (TTM):** {info.get('trailingPE', 'N/A')}")
            st.write(f"**EPS (TTM):** {info.get('trailingEps', 'N/A')}")
        with col5:
            st.write(f"**Earnings Date:** {info.get('earningsDate', 'N/A')}")
            st.write(f"**Forward Dividend & Yield:** {info.get('dividendYield', 'N/A')}")
            st.write(f"**Ex-Dividend Date:** {info.get('exDividendDate', 'N/A')}")
            st.write(f"**1y Target Est:** {info.get('targetMeanPrice', 'N/A')}")

        # Plotting the data with volume
        st.subheader("Stock Price and Volume Over Time")
        fig, ax1 = plt.subplots()

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Close Price', color='tab:blue')
        ax1.plot(data.index, data['Close'], color='tab:blue', label='Close Price')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Volume', color='tab:red')
        ax2.fill_between(data.index, data['Volume'], color='tab:red', alpha=0.3, label='Volume')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        # Format date ticks based on interval
        if interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m']:
            date_format = '%H:%M %p'
        elif interval in ['1d', '5d', '1wk', '1mo', '3mo']:
            date_format = '%Y-%m-%d'
        else:
            date_format = '%Y-%m-%d'

        ax1.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
        fig.autofmt_xdate()

        fig.tight_layout()
        st.pyplot(fig)

        # Display the data
        st.write(data)
    else:
        st.sidebar.error("No data found for the given ticker, period, and interval.")

# Format ticker based on selected market
formatted_ticker = format_ticker(ticker_input, market)

# Fetch and display data for the main ticker input
if ticker_input:
    display_stock_data(formatted_ticker, period, interval)

# Fetch and display data for selected sidebar stock
if selected_sidebar_stock and selected_sidebar_stock != ticker_input:
    st.subheader(f"Data for {selected_sidebar_stock}")
    display_stock_data(format_ticker(selected_sidebar_stock, market), period, interval)
