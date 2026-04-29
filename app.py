import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

st.title("📊 Real-Time Stock Market Dashboard")

# Sidebar inputs
st.sidebar.header("Stock Selection")

stock_symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")
period = st.sidebar.selectbox("Select Period", ["1d", "5d", "1mo", "6mo", "1y", "5y"])
interval = st.sidebar.selectbox("Select Interval", ["1m", "5m", "15m", "1h", "1d"])

# Fetch data
@st.cache_data(ttl=60)
def load_data(symbol, period, interval):
    stock = yf.Ticker(symbol)
    df = stock.history(period=period, interval=interval)
    df.reset_index(inplace=True)
    return df

data = load_data(stock_symbol, period, interval)

if data.empty:
    st.error("No data found. Try another stock symbol.")
    st.stop()

# --- Stock Info ---
col1, col2, col3 = st.columns(3)

latest_price = data["Close"].iloc[-1]
open_price = data["Open"].iloc[0]
change = latest_price - open_price
change_pct = (change / open_price) * 100

col1.metric("Latest Price", f"${latest_price:.2f}")
col2.metric("Change", f"{change:.2f}")
col3.metric("Change %", f"{change_pct:.2f}%")

# --- Candlestick Chart ---
st.subheader("📈 Candlestick Chart")

fig = go.Figure(
    data=[
        go.Candlestick(
            x=data["Datetime"] if "Datetime" in data.columns else data["Date"],
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"]
        )
    ]
)

fig.update_layout(height=600, xaxis_rangeslider_visible=False)

st.plotly_chart(fig, use_container_width=True)

# --- Volume Chart ---
st.subheader("📊 Volume Analysis")

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=data["Datetime"] if "Datetime" in data.columns else data["Date"],
    y=data["Volume"],
    name="Volume"
))

fig2.update_layout(height=300)

st.plotly_chart(fig2, use_container_width=True)

# --- Raw Data ---
st.subheader("📄 Raw Data")
st.dataframe(data)