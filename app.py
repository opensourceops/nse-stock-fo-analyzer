import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
from io import StringIO

# Define the StockDataProcessor class
class StockDataProcessor:
    def __init__(self):
        self.previous_ranks = pd.DataFrame()
        self.upload_count = 0

    def process_stock_data(self, df):
        self.upload_count += 1

        # Clean the column names
        df.columns = df.columns.str.strip()

        # Ensure required columns exist
        required_columns = ['symbol', 'open', 'dayHigh', 'dayLow', 'yearHigh', 'pChange']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise KeyError(f"The following required columns are missing: {', '.join(missing_columns)}")

        # Sort by pChange
        df_sorted = df.sort_values(by='pChange', ascending=False)

        # Rank based on pChange
        rank_column_name = f"Rank {self.upload_count}"
        df_sorted[rank_column_name] = df_sorted['pChange'].rank(ascending=False, method='first').astype(int)

        # Add previous ranks to the new data
        if not self.previous_ranks.empty:
            df_sorted = df_sorted.merge(
                self.previous_ranks,
                on='symbol',
                how='left'
            )

        # Update the previous ranks with the current ranks
        self.previous_ranks = df_sorted[['symbol'] + [col for col in df_sorted.columns if col.startswith('Rank')]]

        # Create 'Action' column based on 'open' and 'dayHigh' columns
        df_sorted['Action'] = df_sorted.apply(
            lambda row: 'sell' if row['open'] == row['dayHigh'] else 'buy' if row['open'] == row['dayLow'] else '', axis=1
        )

        # Create '52_Weeks_High_Status' column based on 'dayHigh' and 'yearHigh' columns
        df_sorted['52_Weeks_High_Status'] = df_sorted.apply(
            lambda row: 'Reached' if row['dayHigh'] == row['yearHigh'] else 'No', axis=1
        )

        # Create '52_Weeks_Low_Status' column based on 'dayLow' and 'yearLow' columns
        df_sorted['52_Weeks_Low_Status'] = df_sorted.apply(
            lambda row: 'Reached' if row['dayLow'] == row['yearLow'] else 'No', axis=1
        )

        return df_sorted

# Initialize processor
processor = StockDataProcessor()

# Create a session object
session = requests.Session()

# Define the URL and headers for the initial request to get cookies
initial_url = 'https://www.nseindia.com'
initial_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# Perform an initial request to the main page to get the cookies
session.get(initial_url, headers=initial_headers)

# Define the URL and headers for the API request
api_url = 'https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O'
api_headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'referer': 'https://www.nseindia.com/market-data/live-equity-market',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# Function to fetch data using the session
def fetch_data():
    response = session.get(api_url, headers=api_headers)
    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        st.error(f"Failed to retrieve data: {response.status_code}")
        return []

# Streamlit UI
st.title("NSE - Securities in Futures and Options")
st.subheader("                    Powered by OpenSourceOps Team")
# Time limit for data fetching in seconds (30 minutes)
REFRESH_INTERVAL = 1800  # 30 minutes

# Placeholder for countdown, data, and download
countdown_placeholder = st.empty()
data_placeholder = st.empty()
download_placeholder = st.empty()

# Columns to keep
columns_to_keep = [
    "symbol", "open", "dayHigh", "dayLow", "previousClose", "lastPrice",
    "change", "pChange", "totalTradedVolume", "totalTradedValue", 
    "yearHigh", "yearLow", "perChange30d", "perChange365d"
]

# Function to display countdown timer
def countdown_timer(interval):
    while interval:
        mins, secs = divmod(interval, 60)
        countdown_placeholder.write(f"Time until next update: {mins:02d}:{secs:02d}")
        time.sleep(1)
        interval -= 1

# Function to generate file name with current date and time
def get_file_name():
    now = datetime.now()
    return now.strftime("nse_fo_data_%Y%m%d_%H%M%S.csv")

# Initial data fetch and processing
data_entries = fetch_data()
df = pd.DataFrame(data_entries)
df_filtered = df[columns_to_keep]
processed_data = processor.process_stock_data(df_filtered)
data_placeholder.write(processed_data)

# Convert DataFrame to CSV and create a download button
csv = processed_data.to_csv(index=False)
download_placeholder.download_button(
    label="Download processed data as CSV",
    data=csv,
    file_name=get_file_name(),
    mime='text/csv'
)

# Update data every 30 minutes with a countdown timer
while True:
    countdown_timer(REFRESH_INTERVAL)
    data_entries = fetch_data()
    df = pd.DataFrame(data_entries)
    df_filtered = df[columns_to_keep]
    processed_data = processor.process_stock_data(df_filtered)
    data_placeholder.write(processed_data)

    # Update CSV and download button with new file name
    csv = processed_data.to_csv(index=False)
    download_placeholder.download_button(
        label="Download processed data as CSV",
        data=csv,
        file_name=get_file_name(),
        mime='text/csv'
    )
