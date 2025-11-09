import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Ask user for tickers (comma-separated)
tickers_input = input("Enter the tickers separated by commas (e.g. CSL.AX, NVDA): ")
tickers = [ticker.strip() for ticker in tickers_input.split(",")]

# Ask user for time frame in years
years_input = input("Enter the time frame in years (e.g., 2 for last 2 years): ")
try:
    years = float(years_input)
except ValueError:
    print("Invalid input. Defaulting to 2 years.")
    years = 2

# Calculate start and end dates
end_date = datetime.now()
start_date = end_date - timedelta(days=years*365)

# Fetch closing prices
close_df = pd.DataFrame()
for ticker in tickers:
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    if not stock_data.empty:
        close_df[ticker] = stock_data['Close']
    else:
        print(f"Warning: No data found for {ticker}")

# Display the closing prices DataFrame
print(close_df)

# Calculate daily returns
returns = close_df.pct_change().dropna()
print (returns)

# Calculate & display the correlation matrix
correlation_matrix = returns.corr()
correlation_matrix = correlation_matrix.round(2)
print(correlation_matrix)

# Plot heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="RdYlGn", linewidths=0.5, vmin=-1, vmax=1)
plt.title("Correlation Matrix of Daily Returns")
plt.show()