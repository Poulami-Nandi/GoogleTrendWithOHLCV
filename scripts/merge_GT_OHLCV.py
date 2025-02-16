import pandas as pd
import numpy as np
import yfinance as yf
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import time  # Import the time module for pausing

# Download Google Trends Data (as a function)
def download_trend_data(search_term, timeframe='today 3-m', geo='', gprop=''):
    """
    Downloads Google Trends data for a given search term and timeframe.

    Parameters:
    search_term (str): The term to query in Google Trends (e.g., "Tesla stock").
    timeframe (str): Timeframe for the trends data (e.g., 'today 3-m', '2020-01-01 2021-12-31').
    geo (str): Geographical region for the trends (e.g., 'US').
    gprop (str): The property type (e.g., 'news' for news-related trends).

    Returns:
    pd.DataFrame: DataFrame containing the Google Trends data.
    """
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([search_term], cat=0, timeframe=timeframe, geo=geo, gprop=gprop)
    trend_data = pytrends.interest_over_time()

    return trend_data

# Calculate trend percetnage
def calculate_trend_percentage(trend_data):
    """
    Calculates the percentage change in the trend over the given period.

    Parameters:
    trend_data (pd.Dataframe): The Dataframe for Google Trends data for a given stock.

    Returns:
    pd.DataFrame: DataFrame containing the Google Trends data with Trend_Percentage column added.
    """
    trend_data['Trend_Percentage'] = trend_data['Tesla stock'].pct_change() * 100
    return trend_data

# Download OHLCV data from Yahoo Finance
def download_ohlcv_data(ticker, start_date, end_date):
    """
    Downloads OHLCV data from Yahoo Finance.

    Parameters:
    ticker (str): The stock ticker (e.g., 'TSLA' for Tesla).
    start_date (str): Start date of the data in 'YYYY-MM-DD' format.
    end_date (str): End date of the data in 'YYYY-MM-DD' format.

    Returns:
    pd.DataFrame: DataFrame containing OHLCV data.
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def align_data(trend_data, stock_data):
    """
    Aligns Google Trends data with stock OHLCV data based on the date index.

    Parameters:
    trend_data (pd.DataFrame): DataFrame containing Google Trends data.
    stock_data (pd.DataFrame): DataFrame containing OHLCV data.

    Returns:
    pd.DataFrame: Merged DataFrame with both Google Trends and stock OHLCV data.
    """
    # Reset index of stock_data to single-level index with 'Date' as a column
    stock_data = stock_data.reset_index()

    # Convert 'Date' column in both trend_data and stock_data to datetime format (if not already)
    trend_data.index = pd.to_datetime(trend_data.index)  # Make sure trend_data index is datetime
    # Reset the index to make 'Date' a column instead of an index
    trend_data.reset_index(inplace=True)
    # Rename the newly created index column to 'Date'
    trend_data.rename(columns={'index': 'Date'}, inplace=True)
    print("Trend Data Head:")
    print(trend_data.head())
    # Rename the column name from date to Date in trend data
    trend_data.columns = trend_data.columns.str.replace('date', 'Date')
    # Convert the 'Date' column in trend_data to datetime (if it's not already)
    trend_data['Date'] = pd.to_datetime(trend_data['Date'])

    stock_data['Date'] = pd.to_datetime(stock_data['Date'])  # Convert stock_data 'Date' column to datetime
    # Flatten the multi-level column index into single-level
    stock_data.columns = ['_'.join(col) for col in stock_data.columns]

    # Dynamically detect the second level of the column name (which is the ticker symbol)
    ticker_symbol = stock_data.columns[-1].split('_')[1]  # Extract the ticker symbol from the first column name
    print(f"Detected ticker symbol: {ticker_symbol}")
    # Replace the ticker symbol dynamically from all column names
    stock_data.columns = stock_data.columns.str.replace(f"_{ticker_symbol}", "")

    # Rename the 'Date_' column to 'Date'
    stock_data.columns = stock_data.columns.str.replace('Date_', 'Date')
    # Ensure that both 'Date' columns are of type datetime64[ns]
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])  # Convert 'Date' in stock_data to datetime64
    trend_data['Date'] = pd.to_datetime(trend_data['Date'])  # Convert 'Date' in trend_data to datetime64


    print("\nStock Data Info:")
    print(stock_data.info())
    print("\ntrend Data Info:")
    print(trend_data.info())
    # Merge Google Trends and OHLCV data on the 'Date' column
    merged_data = pd.merge(stock_data, trend_data, on='Date', how='inner')

    # Set 'Date' column as index for merged_data
    merged_data = merged_data.set_index('Date')

    # Ensure there are no missing values
    merged_data = merged_data.dropna()

    return merged_data

# Normalize stock volume
def normalize_volume(stock_data):
    """
    Normalizes the volume of the stock data.

    Parameters:
    stock_data (pd.DataFrame): DataFrame containing OHLCV data.

    Returns:
    pd.DataFrame: DataFrame with normalized volume.
    """
    volume_min = stock_data['Volume'].min()
    volume_max = stock_data['Volume'].max()
    stock_data['VolumeNormalized'] = ((stock_data['Volume'] - volume_min) / (volume_max - volume_min)) * 100
    return stock_data

# Calculate correlation
def calculate_correlation(merged_data):
    """
    Calculate Pearson correlation between Google Trends data and stock OHLCV data.

    Parameters:
    merged_data (pd.DataFrame): DataFrame containing both Google Trends and OHLCV data.

    Returns:
    pd.Series: Correlation between Google Trends and stock OHLCV columns.
    """
    # Correlate Google Trends data ('Trend_Percentage') with stock data
    correlation = merged_data.corr()

    return correlation

# Step 5: Visualization (optional)
def plot_correlation(merged_data):
    """
    Visualizes the relationship between Google Trends and stock data.

    Parameters:
    merged_data (pd.DataFrame): DataFrame containing both Google Trends and stock OHLCV data.
    """
    print("\nMerged Data Head:")
    print(merged_data.head())  # Print the first few rows of merged_data
    volume_min = merged_data['Volume'].min()
    volume_max = merged_data['Volume'].max()
    merged_data['VolumeNormalized'] = ((merged_data['Volume'] - volume_min) / (volume_max - volume_min)) * 100

    # Plot Google Trends data vs stock close price
    plt.figure(figsize=(12, 6))
    plt.plot(merged_data.index, merged_data['Trend_Percentage'], label='Google Trends change %', color='blue')
    plt.plot(merged_data.index, merged_data['Tesla stock'], label='Google Trends', color='red')
    plt.plot(merged_data.index, merged_data['Close'], label='Stock Close Price', color='green')
    plt.plot(merged_data.index, merged_data['VolumeNormalized'], label='Normalized Volume upto 100', color='orange')
    plt.title('Google Trends vs Stock Price (Close)', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    

# Example Usage
if __name__ == "__main__":
    # Download Google Trends data for "Tesla stock" over the past 3 months (daily data)
    trend_df = download_trend_data('Tesla stock', timeframe='today 3-m')

    # Calculate trend percentage
    trend_df = calculate_trend_percentage(trend_df)

    # Download stock OHLCV data for Tesla
    stock_data = download_ohlcv_data('TSLA', start_date='2024-11-15', end_date='2025-02-15')

    # Normalize Volume data
    #stock_data = normalize_volume(stock_data)

    # Align the data
    merged_data = align_data(trend_df, stock_data)

    # Calculate the correlation between Google Trends and stock data
    correlation = calculate_correlation(merged_data)
    print("Correlation between Google Trends and Stock Data:")
    print(correlation)

    # Plot the trends and stock data
    plot_correlation(merged_data)
