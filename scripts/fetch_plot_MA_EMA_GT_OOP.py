import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from datetime import date, timedelta

class StockTrendAnalysis:
    def __init__(self, search_term, timeframe='today 7-d', geo='', gprop=''):
        """
        Initializes the StockTrendAnalysis class with the search term and trend parameters.
        
        Parameters:
        search_term (str): The search term to query on Google Trends.
        timeframe (str): Timeframe for the trends (default is 'now 7-d').
        geo (str): Geographical region (default is empty for global data).
        gprop (str): Type of data (default is empty for general search data).
        """
        self.search_term = search_term
        self.timeframe = timeframe
        self.geo = geo
        self.gprop = gprop
        self.trend_data = None
    
    def download_trend_data(self):
        """
        Downloads Google Trends data for a given search term, timeframe, and other parameters.
        
        Returns:
        pd.DataFrame: A DataFrame containing the trend data for the search term.
        """
        pytrends = TrendReq(hl='en-US', tz=360)  # Initialize pytrends object
        pytrends.build_payload([self.search_term], cat=0, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)
        
        # Download interest over time data
        self.trend_data = pytrends.interest_over_time()
        return self.trend_data
    
    def calculate_ema(self, trend_data, window=3):
        """
        Calculates the Exponential Moving Average (EMA) of the trend data.
        
        Parameters:
        trend_data (pd.Series): The time series of Google Trends data for a given stock.
        window (int): The window size for the EMA calculation.
        
        Returns:
        pd.Series: The EMA values.
        """
        return trend_data.ewm(span=window, adjust=False).mean()
    
    def trend_analysis(self, moving_average_window=3):
        """
        Analyzes the trend direction of a given stock based on Google Trends data.
        
        Parameters:
        moving_average_window (int): The window size for calculating the moving average.
        
        Returns:
        str: Sentiment of the stock trend ('Positive', 'Negative', 'Neutral')
        """
        trend_data_ma = self.trend_data[self.search_term].rolling(window=moving_average_window).mean() # Access the correct column by name

        # Get the first and last valid (non-NaN) values from the moving average Series
        start_value = trend_data_ma.dropna().iloc[0]  
        end_value = trend_data_ma.dropna().iloc[-1]
        
        if end_value > start_value:
            sentiment = 'Positive'
        elif end_value < start_value:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return sentiment

    
    def percentage_trend_analysis(self):
        """
        Analyzes the percentage change in the stock trend over the given period.
        
        Returns:
        float: Percentage change in trend
        str: Sentiment based on percentage change ('Positive', 'Negative', 'Neutral')
        """
        # Access the specific column using the search term
        start_value = self.trend_data[self.search_term].iloc[0]  
        end_value = self.trend_data[self.search_term].iloc[-1]
        percentage_change = ((end_value - start_value) / start_value) * 100
        
        if percentage_change > 0:
            sentiment = 'Positive'
        elif percentage_change < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return percentage_change, sentiment

    
    def visualize_trend(self, moving_average_window=3, ema_window=3):
      """
        Visualizes the trend of a given stock with the moving average, EMA, and original trend data.

      Parameters:
      moving_average_window (int): The window size for calculating the moving average.
      ema_window (int): The window size for calculating the Exponential Moving Average.
      """
      # Step 1: Calculate the moving average for the trend data
      trend_data_ma = self.trend_data.rolling(window=moving_average_window).mean()
    
      # Step 2: Calculate the Exponential Moving Average (EMA)
      trend_data_ema = self.calculate_ema(self.trend_data, window=ema_window)
    
      # Step 3: Plot the raw trend data, the moving average, and the EMA on the same graph
      plt.figure(figsize=(10, 6))
    
      # Plot Original Trend Data with label
      plt.plot(self.trend_data, label='Original Trend Data', color='blue', alpha=0.7)
    
      # Plot Moving Average with label
      plt.plot(trend_data_ma, label=f'Moving Average ({moving_average_window} Days)', color='orange', linestyle='--')
    
      # Plot Exponential Moving Average (EMA) with label
      plt.plot(trend_data_ema, label=f'Exponential Moving Average ({ema_window} Days)', color='green', linestyle='-.')
    
      # Step 4: Add labels, title, and legends
      plt.title(f'{self.search_term} Interest Over Time (Google Trends)', fontsize=14)
      plt.xlabel('Date', fontsize=12)
      plt.ylabel('Interest Level', fontsize=12)
      plt.xticks(rotation=45)
    
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
    trend_analysis_obj = StockTrendAnalysis(search_term='Tesla stock', timeframe=StockTrendAnalysis.get_timeframe(20))

    # Download Google Trends data for "Tesla stock" over the past 20 days
    trend_data = trend_analysis_obj.download_trend_data()

    # Perform trend analysis and print the result
    sentiment = trend_analysis_obj.trend_analysis(moving_average_window=3)
    print(f"Trend Analysis Sentiment: {sentiment}")

    # Perform percentage trend analysis and print the result
    percentage_change, sentiment_percentage = trend_analysis_obj.percentage_trend_analysis()
    print(f"Percentage Trend Analysis: {percentage_change:.2f}%")
    print(f"Sentiment from Percentage Change: {sentiment_percentage}")

    # Visualize the trend with moving average and EMA
    trend_analysis_obj.visualize_trend(moving_average_window=3, ema_window=3)
