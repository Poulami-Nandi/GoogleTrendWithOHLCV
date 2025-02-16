import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from datetime import date, timedelta

# Function to download Google Trends data for a given term and time period
def download_trend_data(search_term, timeframe='now 7-d', geo='', gprop=''):
    """
    Downloads Google Trends data for a given search term, timeframe, and other parameters.

    Parameters:
    search_term (str): The search term to query on Google Trends.
    timeframe (str): Timeframe for the trends (e.g., 'now 7-d', 'today 3-m', '2020-01-01 2021-12-31').
    geo (str): Geographical region (e.g., 'US' for the United States). Leave empty for global data.
    gprop (str): Type of data (e.g., '' for general search data, 'news', 'images', etc.).

    Returns:
    pd.DataFrame: A DataFrame containing the trend data for the search term.
    """

    pytrends = TrendReq(hl='en-US', tz=360)  # Initialize pytrends object
    pytrends.build_payload([search_term], cat=0, timeframe=timeframe, geo=geo, gprop=gprop)

    # Download interest over time data
    trend_data = pytrends.interest_over_time()

    # Return the DataFrame containing trend data
    return trend_data


# Function to calculate Exponential Moving Average (EMA)
def calculate_ema(trend_data, window=3):
    """
    Calculates the Exponential Moving Average (EMA) of the trend data.

    Parameters:
    trend_data (pd.Series): The time series of Google Trends data for a given stock.
    window (int): The window size for the EMA calculation.

    Returns:
    pd.Series: The EMA values.
    """
    return trend_data.ewm(span=window, adjust=False).mean()


# Function for Trend Analysis (based on the trend direction)
def trend_analysis(trend_data, moving_average_window=3):
    """
    Analyzes the trend direction of a given stock based on Google Trends data.

    Parameters:
    trend_data (pd.Series): The time series of Google Trends data for a given stock.
    moving_average_window (int): The window size for calculating the moving average.

    Returns:
    str: Sentiment of the stock trend ('Positive', 'Negative', 'Neutral')
    """

    # Step 1: Calculate the moving average to smooth out fluctuations
    trend_data_ma = trend_data.rolling(window=moving_average_window).mean()

    # Step 2: Compare the start and end values of the moving average to determine trend direction
    start_value = trend_data_ma.iloc[0]
    end_value = trend_data_ma.iloc[-1]

    # Step 3: Determine sentiment based on trend direction
    if end_value > start_value:
        sentiment = 'Positive'
    elif end_value < start_value:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return sentiment


# Function for Percentage Trend Analysis (percentage change between first and last value)
def percentage_trend_analysis(trend_data):
    """
    Analyzes the percentage change in the stock trend over the given period.

    Parameters:
    trend_data (pd.Series): The time series of Google Trends data for a given stock.

    Returns:
    float: Percentage change in trend
    str: Sentiment based on percentage change ('Positive', 'Negative', 'Neutral')
    """

    # Step 1: Calculate the percentage change from the first to the last value
    start_value = trend_data.iloc[0]
    end_value = trend_data.iloc[-1]
    percentage_change = ((end_value - start_value) / start_value) * 100

    # Step 2: Determine sentiment based on percentage change
    if percentage_change > 0:
        sentiment = 'Positive'
    elif percentage_change < 0:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return percentage_change, sentiment


# Function for Trend Visualization
def visualize_trend(trend_data, moving_average_window=3, ema_window=3):
    """
    Visualizes the trend of a given stock with the moving average, EMA, and original trend data.

    Parameters:
    trend_data (pd.Series): The time series of Google Trends data for a given stock.
    moving_average_window (int): The window size for calculating the moving average.
    ema_window (int): The window size for calculating the Exponential Moving Average.
    """

    # Step 1: Calculate the moving average for the trend data
    trend_data_ma = trend_data.rolling(window=moving_average_window).mean()

    # Step 2: Calculate the Exponential Moving Average (EMA)
    trend_data_ema = calculate_ema(trend_data, window=ema_window)

    # Step 3: Plot the raw trend data, the moving average, and the EMA on the same graph
    plt.figure(figsize=(10, 6))
    plt.plot(trend_data, label='Original Trend Data', color='blue', alpha=0.7)
    plt.plot(trend_data_ma, label=f'Moving Average ({moving_average_window} Days)', color='orange', linestyle='--')
    plt.plot(trend_data_ema, label=f'Exponential Moving Average ({ema_window} Days)', color='green', linestyle='-.')

    # Step 4: Add labels, title, and legends
    plt.title('Stock Interest Over Time (Google Trends)', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Interest Level', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def get_timeframe(days_back):
    """
    Generates a Google Trends timeframe string for the specified number of days back.

    The timeframe ends on today and goes back 'days_back' days.

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
    # Download Google Trends data for "Tesla stock" over the past 20 days
    trend_df = download_trend_data('Tesla stock', timeframe=get_timeframe(20))

    # Check if data is available (if empty, handle appropriately)
    if trend_df.empty:
        print("No trend data available for the given term.")
    else:
        # Perform trend analysis and print the result
        sentiment = trend_analysis(trend_df['Tesla stock'], moving_average_window=3)
        print(f"Trend Analysis Sentiment: {sentiment}")

        # Perform percentage trend analysis and print the result
        percentage_change, sentiment_percentage = percentage_trend_analysis(trend_df['Tesla stock'])
        print(f"Percentage Trend Analysis: {percentage_change:.2f}%")
        print(f"Sentiment from Percentage Change: {sentiment_percentage}")

        # Visualize the trend with moving average and EMA
        visualize_trend(trend_df['Tesla stock'], moving_average_window=3, ema_window=3)
