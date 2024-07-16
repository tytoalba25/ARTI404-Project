#streamlit run stock2.py

import streamlit as st
import yfinance as yf
#from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

# # Database setup
# DATABASE_URI = 'sqlite:///stocks.db'
# engine = create_engine(DATABASE_URI)

# Initialize session state
if 'last_10_stocks' not in st.session_state:
    st.session_state['last_10_stocks'] = []

# Function to fetch live stock data
def fetch_stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist

# Function to save data to database
# def save_to_database(df, table_name):
#     df.to_sql(table_name, con=engine, if_exists='append', index=True)

# Function to update last 10 stocks
def update_last_10_stocks(ticker):
    if ticker not in st.session_state['last_10_stocks']:
        st.session_state['last_10_stocks'].append(ticker)
        if len(st.session_state['last_10_stocks']) > 10:
            st.session_state['last_10_stocks'].pop(0)

# Sidebar
st.sidebar.title("Last 10 Stocks")
selected_sidebar_stock = st.sidebar.radio("Select a stock:", st.session_state['last_10_stocks'])

# Main page
st.title("Live Stock Market Data")

ticker = st.text_input("Enter stock ticker (e.g., AAPL, GOOGL):")
period = st.selectbox("Select period:", ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'])

if ticker:
    data = fetch_stock_data(ticker, period)
    if not data.empty:
        st.write(data)
        #save_to_database(data, ticker)
        update_last_10_stocks(ticker)
        st.success(f"Data for {ticker} has been saved to the database.")
    else:
        st.error("No data found for the given ticker and period.")

# Fetch and display data for selected sidebar stock
if selected_sidebar_stock:
    st.subheader(f"Data for {selected_sidebar_stock}")
    sidebar_data = fetch_stock_data(selected_sidebar_stock, period)
    if not sidebar_data.empty:
        st.write(sidebar_data)
        
        # Plotting the data
        st.subheader("Stock Price Over Time")
        st.line_chart(sidebar_data['Close'])
    else:
        st.error(f"No data found for {selected_sidebar_stock}.")

# Option to view stored data
# st.subheader("View Stored Data")
# tables = engine.table_names()
# selected_table = st.selectbox("Select table (ticker):", tables)
# if selected_table:
#     query = f"SELECT * FROM {selected_table}"
#     stored_data = pd.read_sql(query, con=engine)
#     st.write(stored_data)
