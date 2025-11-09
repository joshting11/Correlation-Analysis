import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.title("📊 Stock Correlation Analyzer")

# --- User Inputs ---
tickers_input = st.text_input("Enter tickers separated by commas (e.g. CSL.AX, NVDA, AAPL):")
years = st.number_input("Enter the time frame in years:", min_value=0.1, max_value=10.0, value=2.0, step=0.5)

if tickers_input:
    tickers = [ticker.strip() for ticker in tickers_input.split(",")]

    # --- Date Range ---
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)

    st.write(f"📅 Fetching data from {start_date.date()} to {end_date.date()}")

    # --- Fetch Data ---
    close_df = pd.DataFrame()
    for ticker in tickers:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        if not stock_data.empty:
            close_df[ticker] = stock_data['Close']
        else:
            st.warning(f"No data found for {ticker}")

    # --- Show Price Data ---
    st.subheader("Closing Prices")
    st.dataframe(close_df.tail())

    # --- Calculate Returns ---
    returns = close_df.pct_change().dropna()

    st.subheader("Daily Returns")
    st.dataframe(returns.tail())

    # --- Correlation Matrix ---
    correlation_matrix = returns.corr().round(2)

    st.subheader("Correlation Matrix")
    st.dataframe(correlation_matrix)

    # --- Plot Heatmap ---
    st.subheader("Heatmap")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="RdYlGn", linewidths=0.5, vmin=-1, vmax=1, ax=ax)
    plt.title("Correlation Matrix of Daily Returns")
    st.pyplot(fig)

