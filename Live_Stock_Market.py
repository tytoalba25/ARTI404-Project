#streamlit run ../ARTI404-Project/Live_Stock_Market_Phase_4.py 


import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ta

# Initialize session state
if 'last_10_stocks' not in st.session_state:
    st.session_state['last_10_stocks'] = []
if 'interval_options' not in st.session_state:
    st.session_state['interval_options'] = []

# Function to fetch live stock data
def fetch_stock_data(ticker, period, interval):
    stock = yf.Ticker(ticker)
    return stock.history(period=period, interval=interval)

# Function to fetch additional stock info
def fetch_stock_info(ticker):
    stock = yf.Ticker(ticker)
    return stock.info

# Function to update last 10 stocks
def update_last_10_stocks(ticker):
    if ticker not in st.session_state['last_10_stocks']:
        st.session_state['last_10_stocks'].append(ticker)
        if len(st.session_state['last_10_stocks']) > 10:
            st.session_state['last_10_stocks'].pop(0)

def check_ticker(ticker, period, interval):
    data = fetch_stock_data(ticker, period, interval)
    if not data.empty:
        update_last_10_stocks(ticker)
        st.sidebar.success(f"Data for {ticker} has been loaded.")
        return True
    st.sidebar.error("No data found for the given ticker")
    return False

# Sidebar
st.sidebar.image("../ARTI404-Project/stock_logo.png", caption="Stock Logo")
st.sidebar.title("Last 10 Stocks")
selected_sidebar_stock = st.sidebar.radio("Select a stock:", st.session_state['last_10_stocks'], index=0 if st.session_state['last_10_stocks'] else None)

st.sidebar.title("Stock Selection")
market = st.sidebar.selectbox("Select market:", ["US", "Canada", "UK", "Germany", "France", "Japan", "Australia"], index=0)

# Define valid intervals for each period
interval_options = {
    '1d': ['1m', '2m', '5m', '15m', '30m', '60m', '90m'],
    '5d': ['30m', '60m', '90m', '1d'],
    '1mo': ['1d', '5d', '1wk'],
    '3mo': ['1d', '5d', '1wk', '1mo'],
    '6mo': ['1d', '5d', '1wk', '1mo', '3mo'],
    '1y': ['1d', '5d', '1wk', '1mo', '3mo'],
    '2y': ['1d', '5d', '1wk', '1mo', '3mo'],
    '5y': ['1d', '5d', '1wk', '1mo', '3mo'],
    '10y': ['1d', '5d', '1wk', '1mo', '3mo'],
    'ytd': ['90m', '1d', '5d', '1wk', '1mo', '3mo'],
    'max': ['1d', '5d', '1wk', '1mo', '3mo']
}

# Function to update interval options based on selected period
def update_interval_options():
    st.session_state['interval_options'] = interval_options.get(st.session_state['period'], [])

# Period selection in the sidebar
period = st.sidebar.selectbox("Select period:", list(interval_options.keys()), index=1, key='period', on_change=update_interval_options)

# Update interval options based on initial period
if not st.session_state['interval_options']:
    update_interval_options()

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
    if market == "Canada" and ticker.endswith(".V"):
        return ticker
    return ticker + market_suffix[market]

# Function to set date format based on interval
def set_date_format(ax, interval):
    date_format = '%H:%M %p' if interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m'] else '%Y-%m-%d'
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
    ax.figure.autofmt_xdate()

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
        set_date_format(ax1, interval)
        fig.tight_layout()
        st.pyplot(fig)
        st.write(data)
        
        # Technical analysis
        st.subheader("Technical Analysis and Recommendation")
        macd = ta.trend.MACD(data['Close'])
        data['MACD'] = macd.macd()
        data['MACD_Signal'] = macd.macd_signal()
        data['MACD_Diff'] = macd.macd_diff()
        stochastic = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close'])
        data['Stoch'] = stochastic.stoch()
        data['Stoch_Signal'] = stochastic.stoch_signal()
        bb = ta.volatility.BollingerBands(data['Close'])
        data['BB_High'] = bb.bollinger_hband()
        data['BB_Low'] = bb.bollinger_lband()
        
        # Plot the MACD
        fig, ax = plt.subplots()
        ax.plot(data.index, data['MACD'], label='MACD', color='blue')
        ax.plot(data.index, data['MACD_Signal'], label='Signal Line', color='red')
        ax.fill_between(data.index, data['MACD_Diff'], color='gray', alpha=0.3, label='MACD Histogram')
        ax.legend(loc='upper left')
        ax.set_title('MACD')
        set_date_format(ax, interval)
        st.pyplot(fig)
        
        # Plot the Stochastic Oscillator
        fig, ax = plt.subplots()
        ax.plot(data.index, data['Stoch'], label='%K', color='blue')
        ax.plot(data.index, data['Stoch_Signal'], label='%D', color='red')
        ax.legend(loc='upper left')
        ax.set_title('Stochastic Oscillator')
        set_date_format(ax, interval)
        st.pyplot(fig)
        
        # Plot the Bollinger Bands
        fig, ax = plt.subplots()
        ax.plot(data.index, data['Close'], label='Close Price', color='blue')
        ax.plot(data.index, data['BB_High'], label='Upper Band', color='green')
        ax.plot(data.index, data['BB_Low'], label='Lower Band', color='red')
        ax.fill_between(data.index, data['BB_High'], data['BB_Low'], color='gray', alpha=0.3)
        ax.legend(loc='upper left')
        ax.set_title('Bollinger Bands')
        set_date_format(ax, interval)
        st.pyplot(fig)
        
        # Trading Recommendation
        latest_data = data.iloc[-1]
        recommendation = "Hold"
        if latest_data['MACD'] > latest_data['MACD_Signal'] and latest_data['Stoch'] < 20:
            recommendation = "Buy Long"
        elif latest_data['MACD'] < latest_data['MACD_Signal'] and latest_data['Stoch'] > 80:
            recommendation = "Sell Short"
        
        st.subheader(f"Recommendation: {recommendation}")
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
