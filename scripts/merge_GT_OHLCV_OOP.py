import pandas as pd
import numpy as np
import yfinance as yf
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import time
from datetime import date, timedelta


class StockTrendAnalysis:
    def __init__(self, search_term, timeframe='today 3-m', geo='', gprop=''):
        """
        Initializes the StockTrendAnalysis class with the search term and trend parameters.
        
        Parameters:
        search_term (str): The search term to query on Google Trends.
        timeframe (str): Timeframe for the trends (e.g., 'today 3-m').
        geo (str): Geographical region for the trends.
        gprop (str): Type of data (e.g., 'news' for news-related trends).
        """
        self.search_term = search_term
        self.timeframe = timeframe
        self.geo = geo
        self.gprop = gprop
        self.trend_data = None
        self.stock_data = None
        self.merged_data = None
    
    def download_trend_data(self):
        """
        Downloads Google Trends data for a given search term and timeframe.

        Returns:
        pd.DataFrame: A DataFrame containing the trend data for the search term.
        """
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([self.search_term], cat=0, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)
        self.trend_data = pytrends.interest_over_time()
        return self.trend_data
    
    def calculate_trend_percentage(self):
        """
        Calculates the percentage change in the trend over the given period.

        Returns:
        pd.DataFrame: DataFrame containing Google Trends data with Trend_Percentage column.
        """
        self.trend_data['Trend_Percentage'] = self.trend_data['Tesla stock'].pct_change() * 100
        return self.trend_data
    
    def get_timeframe(self, days_back):
        """
        Generates a Google Trends timeframe string for the specified number of days back.
        
        Parameters:
        days_back (int): The number of days to go back from today.
        
        Returns:
        str: The Google Trends timeframe string in the format 'YYYY-MM-DD YYYY-MM-DD'.
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)
        timeframe = f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}"
        return timeframe

    def download_ohlcv_data(self, ticker, start_date, end_date):
        """
        Downloads OHLCV data from Yahoo Finance.

        Parameters:
        ticker (str): The stock ticker (e.g., 'TSLA' for Tesla).
        start_date (str): Start date of the data in 'YYYY-MM-DD' format.
        end_date (str): End date of the data in 'YYYY-MM-DD' format.

        Returns:
        pd.DataFrame: DataFrame containing OHLCV data.
        """
        self.stock_data = yf.download(ticker, start=start_date, end=end_date)
        return self.stock_data

    def align_data(self):
        """
        Aligns Google Trends data with stock OHLCV data based on the date index.

        Returns:
        pd.DataFrame: Merged DataFrame with both Google Trends and stock OHLCV data.
        """
        # Reset index of stock_data to single-level index with 'Date' as a column
        self.stock_data = self.stock_data.reset_index()

        # Convert 'Date' column in both trend_data and stock_data to datetime format
        self.trend_data.index = pd.to_datetime(self.trend_data.index)
        self.trend_data.reset_index(inplace=True)
        # Rename the 'date' column to 'Date' before converting to datetime
        self.trend_data.rename(columns={'date': 'Date'}, inplace=True)  

        # Remove the second level and keep only the first level of the column names
        self.stock_data.columns = self.stock_data.columns.get_level_values(0)
        print("\nStock Data Info:")
        print(self.stock_data.info())
        print("\ntrend Data Info:")
        print(self.trend_data.info()) 

        # Ensure 'Date' columns are datetime type
        self.stock_data['Date'] = pd.to_datetime(self.stock_data['Date'])
        self.trend_data['Date'] = pd.to_datetime(self.trend_data['Date'])

        # Merge Google Trends and OHLCV data on the 'Date' column
        self.merged_data = pd.merge(self.stock_data, self.trend_data, on='Date', how='inner')

        # Set 'Date' column as index for merged_data
        self.merged_data = self.merged_data.set_index('Date')

        # Ensure there are no missing values
        self.merged_data = self.merged_data.dropna()

        return self.merged_data
    
    def normalize_volume(self):
        """
        Normalizes the volume of the stock data.

        Returns:
        pd.DataFrame: DataFrame with normalized volume.
        """
        volume_min = self.merged_data['Volume'].min()
        volume_max = self.merged_data['Volume'].max()
        self.merged_data['VolumeNormalized'] = ((self.merged_data['Volume'] - volume_min) / (volume_max - volume_min)) * 100
        return self.merged_data
    
    def calculate_correlation(self):
        """
        Calculate Pearson correlation between Google Trends data and stock OHLCV data.

        Returns:
        pd.Series: Correlation between Google Trends and stock OHLCV columns.
        """
        correlation = self.merged_data.corr()
        return correlation
    
    def plot_correlation(self):
        """
        Visualizes the relationship between Google Trends and stock data.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.merged_data.index, self.merged_data['Trend_Percentage'], label='Google Trends change %', color='blue')
        plt.plot(self.merged_data.index, self.merged_data['Tesla stock'], label='Google Trends', color='red')
        plt.plot(self.merged_data.index, self.merged_data['Close'], label='Stock Close Price', color='green')
        plt.plot(self.merged_data.index, self.merged_data['VolumeNormalized'], label='Normalized Volume upto 100', color='orange')
        plt.title('Google Trends vs Stock Price (Close)', fontsize=14)
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def get_timeframe(days_back):
        """
        Generates a Google Trends timeframe string for the specified number of days back.
        
        Parameters:
        days_back (int): The number of days to go back from today.
        
        Returns:
        str: The Google Trends timeframe string in the format 'YYYY-MM-DD YYYY-MM-DD'.
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)
        timeframe = f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}"
        return timeframe


# Example Usage
if __name__ == "__main__":
    # Create an instance of StockTrendAnalysis class for "Tesla stock"
    stock_trend_analysis = StockTrendAnalysis(search_term='Tesla stock', timeframe=StockTrendAnalysis.get_timeframe(20))

    # Download Google Trends data for "Tesla stock"
    trend_data = stock_trend_analysis.download_trend_data()

    # Calculate trend percentage
    trend_data = stock_trend_analysis.calculate_trend_percentage()

    # Download stock OHLCV data for Tesla
    stock_data = stock_trend_analysis.download_ohlcv_data(ticker='TSLA', start_date='2024-11-15', end_date='2025-02-15')

    # Align the data
    merged_data = stock_trend_analysis.align_data()

    # Normalize Volume data
    merged_data = stock_trend_analysis.normalize_volume()

    # Calculate the correlation between Google Trends and stock data
    correlation = stock_trend_analysis.calculate_correlation()
    print("Correlation between Google Trends and Stock Data:")
    print(correlation)

    # Plot the trends and stock data
    stock_trend_analysis.plot_correlation()
