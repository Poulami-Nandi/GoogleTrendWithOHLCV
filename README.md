# GoogleTrendWithOHLCV
Merging Google Trend analysis with OHLCV data of a stock to find insights about price movement

## Overview

The `StockTrendAnalysis` project provides a Python class that helps in analyzing stock trends using Google Trends data. It downloads Google Trends data for a specific search term, calculates trend percentages, aligns this data with stock OHLCV data (Open, High, Low, Close, Volume), and provides various analysis and visualizations. This project is ideal for correlating stock price movements with online search interest over time.

## Features

- **Download Google Trends Data**: Downloads Google Trends data for a specified term and timeframe.
- **Calculate Trend Percentages**: Computes the percentage change in Google Trends data.
- **Download OHLCV Stock Data**: Downloads stock data (Open, High, Low, Close, Volume) from Yahoo Finance.
- **Align Data**: Aligns Google Trends data with stock OHLCV data on the 'Date' column.
- **Normalize Volume**: Normalizes the stock volume to a scale between 0 and 100.
- **Correlation Analysis**: Calculates Pearson correlation between Google Trends data and stock OHLCV data.
- **Visualizations**: Visualizes the relationship between Google Trends data and stock data, including trend percentages, stock close prices, and normalized volume.

## Requirements

- Python 3.x
- Libraries:
  - `pandas`
  - `numpy`
  - `yfinance`
  - `pytrends`
  - `matplotlib`

You can install the required libraries using:

```bash
pip install pandas numpy yfinance pytrends matplotlib
```
Class: StockTrendAnalysis
The core of this project is the StockTrendAnalysis class that performs the following tasks:

Methods
__init__(self, search_term, timeframe='today 3-m', geo='', gprop=''):

Initializes the class with the search term and trend parameters.
download_trend_data(self):

Downloads Google Trends data for the specified search term.
calculate_trend_percentage(self):

Calculates the percentage change in Google Trends data.
get_timeframe(self, days_back):

Generates a Google Trends timeframe string for the specified number of days back.
download_ohlcv_data(self, ticker, start_date, end_date):

Downloads stock OHLCV data from Yahoo Finance.
align_data(self):

Aligns Google Trends data with stock OHLCV data by merging on the 'Date' column.
normalize_volume(self):

Normalizes the volume of the stock data between 0 and 100.
calculate_correlation(self):

Calculates Pearson correlation between Google Trends and stock OHLCV data.
plot_correlation(self):

Visualizes the relationship between Google Trends and stock data.
Example Usage
# Example Usage
```bash
if __name__ == "__main__":
    # Create an instance of StockTrendAnalysis class for "Tesla stock"
    stock_trend_analysis = StockTrendAnalysis(search_term='Tesla stock', timeframe='today 3-m')

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
```

Example Output
Correlation Matrix: A printed matrix showing the correlation between Google Trends data and stock OHLCV data.
Plot: A graph displaying the Google Trends data, stock price (close), and normalized volume.
Additional Notes
The project uses PyTrends to fetch Google Trends data.
Yahoo Finance is used to fetch the OHLCV data of stocks.
Matplotlib is used to generate visualizations.
The class supports customizable parameters such as search term, timeframe, and geographical region for Google Trends.
How to Use
Download Google Trends Data:

Initialize an instance of the StockTrendAnalysis class with the stock or term you want to track.
Call download_trend_data() to get the trends for that term.
Download Stock Data:

Use download_ohlcv_data() to fetch stock data for a given ticker.
Data Alignment:

Use align_data() to merge Google Trends data with stock OHLCV data.
Trend Analysis:

Use calculate_trend_percentage() to analyze the percentage change in trends over time.
Call calculate_correlation() to get the correlation between trends and stock data.
Visualization:

Call plot_correlation() to generate visualizations comparing Google Trends data and stock data.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to modify and extend this project to track more stocks or include additional analyses. Happy coding!

### **Explanation of the README**:

- **Overview**: Provides a brief description of the project.
- **Features**: Lists the key features of the project, such as downloading trend data, calculating trend percentages, normalizing volume, etc.
- **Requirements**: Specifies the required Python libraries and how to install them.
- **Class and Methods**: Describes the main class `StockTrendAnalysis` and its methods.
- **Example Usage**: Provides a step-by-step guide on how to use the class and its methods in practice.
- **License**: Mentions the project's licensing information.

This structure gives a comprehensive yet concise description of the project and its functionalities. Let me know if you'd like further details added!





