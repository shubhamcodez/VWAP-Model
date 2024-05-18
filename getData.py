import os
import pandas as pd
import numpy as np
from taq.MyDirectories import MyDirectories
from taq.BinReader import BinReader
from taq.TAQTradesReader import TAQTradesReader
from impactUtils.FirstPriceBuckets import FirstPriceBuckets

# Constants
trade_directory = 'trades/'
startTS = 19 * 60 * 60 * 1000 / 2  # starting timestamp
endTS = 16 * 60 * 60 * 1000  # ending timestamp 
interval_length = 30 * 60 * 1000  # 30 minutes in milliseconds

# Read SP500 stock symbols
sp500_file_path = 'SP500.txt'
with open(sp500_file_path, 'r') as file:
    sp500_stocks = [line.strip() for line in file]

# Initialize matrices to store computed values
num_stocks = len(sp500_stocks)
num_days = len(os.listdir(trade_directory))
num_intervals_per_day = 13

# Initialize matrices for intervals data
price_data = np.zeros((num_stocks, num_days * num_intervals_per_day))
volume_data = np.zeros((num_stocks, num_days * num_intervals_per_day))

# Iterate over each subfolder within the trade directory
for day_index, trade_day in enumerate(os.listdir(trade_directory)):
    trade_day_path = os.path.join(trade_directory, trade_day)

    for stock_index, stock_symbol in enumerate(sp500_stocks):
        try:
            trades = TAQTradesReader(trade_day_path + f'/{stock_symbol}_trades.binRT')
        except FileNotFoundError:
            print(f"No trade data found for {stock_symbol}. Skipping...")
            continue

        timestamps = np.array([trades.getTimestamp(i) for i in range(trades.getN())])
        prices = np.array([trades.getPrice(i) for i in range(trades.getN())])
        volumes = np.array([trades.getSize(i) for i in range(trades.getN())])

        currentTS = startTS
        interval_index = 0
        while currentTS < endTS:
            nextTS = currentTS + interval_length
            mask = (timestamps >= currentTS) & (timestamps < nextTS)

            interval_prices = prices[mask]
            interval_volumes = volumes[mask]

            average_price = interval_prices.mean() if interval_prices.size > 0 else 0
            cumulative_volume = interval_volumes.sum()

            price_data[stock_index, day_index * num_intervals_per_day + interval_index] = average_price
            volume_data[stock_index, day_index * num_intervals_per_day + interval_index] = cumulative_volume

            currentTS = nextTS
            interval_index += 1

# Create column names for the DataFrames
price_column_names = ['stock_name'] + [
    f'day_{day_index+1}_interval_{interval_index+1}_avg_price' 
    for day_index in range(num_days) 
    for interval_index in range(num_intervals_per_day)
]

volume_column_names = ['stock_name'] + [
    f'day_{day_index+1}_interval_{interval_index+1}_cum_volume' 
    for day_index in range(num_days) 
    for interval_index in range(num_intervals_per_day)
]

# Combine stock names with their respective data
price_flat_data = np.hstack((np.array(sp500_stocks).reshape(-1, 1), price_data))
volume_flat_data = np.hstack((np.array(sp500_stocks).reshape(-1, 1), volume_data))

# Create DataFrames
price_df = pd.DataFrame(price_flat_data, columns=price_column_names)
volume_df = pd.DataFrame(volume_flat_data, columns=volume_column_names)

# Save the DataFrames to CSV files
price_df.to_csv('price_results.csv', index=False)
volume_df.to_csv('volume_results.csv', index=False)
