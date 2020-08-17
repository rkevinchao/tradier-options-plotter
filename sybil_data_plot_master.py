"""
sybil_data_plot_master.py
Last Modified: August 16, 2020
Description: This script handles all the plotting for run_sybil_plotter.py

# mplfinance style documentation
# https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb
"""

from datetime import datetime
import time
import pandas as pd
import mplfinance as mpf


# Are we plotting intraday or daily data. 
def plot_data(data, should_use_history_endpoint, data_title, settings):
    if (should_use_history_endpoint):
        plot_history(data, data_title, settings)
    else:
        plot_timesales(data, data_title, settings)
    return 0


# Make a plot of daily or longer data
def plot_history(data, data_title, settings):
    ohlc = [] # list of candlestick chart data
    
    if (type(data) == type({})):
        print("Insufficient trade data. Printing all data and terminating Program.")
        print(data)
        exit()
    
    for quote in data:
        quote_time = datetime.strptime(quote['date'], "%Y-%m-%d")
        pandas_data = quote_time, quote['open'], quote['high'], quote['low'], quote['close'], quote['volume']
        ohlc.append(pandas_data)

    if (len(ohlc)): #if there is any data
        df = pd.DataFrame(ohlc)
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df.set_index(pd.DatetimeIndex(df['Date']))

        ohlc_dict = {
            'Open':'first',
            'High':'max',
            'Low':'min',
            'Close':'last',
            'Volume':'sum'
        }

        df = df.resample(settings['historyBinning']).agg(ohlc_dict)
        #df = df.resample('1W').agg(ohlc_dict) #for longer dated options

        # Drop-weekends. Need to be careful about this if we sample by weekend.
        for index, row in df.iterrows():
            day_num = index.to_pydatetime().weekday()
            if (day_num > 4): # weekend
                df.drop(index, inplace=True)
        
        if (settings['shouldPrintData']):
            pd.set_option('display.max_rows', None)
            print(df)
        
        s  = mpf.make_mpf_style(base_mpf_style='yahoo', 
                                rc={'font.size':10,
                                    'font.weight':'light',
                                    'axes.edgecolor':'black',
                                    'figure.figsize':(8.0, 4.8)
                                    }, 
                                y_on_right=False,
                                facecolor='w',
                                gridstyle=settings['gridstyle']
                                )
                
        
        kwargs = dict(type='candle',volume=True)        
        mpf.plot(df, **kwargs, style=s, 
                title=dict(title="\n\n" + data_title, weight='regular', size=11),                
                datetime_format=' %m/%d',
                tight_layout=settings['tight_layout'],
                block=True,
                ylabel="Option Price ($)")
        # Note: (show_nontrading = False) didn't work, had to custom resample and drop.
    else:
        print("No option trades during period.")
    
    return

# Make a candlestick plot of intraday data.
def plot_timesales(data, data_title, settings):    
    ohlc = [] # list of candlestick chart data
    
    if (type(data) == type({})):
        print("Insufficient trade data. Printing all data and terminating Program.")
        print(data)
        exit()
    
    # Organize the data
    for quote in data:
        quote_time = datetime.strptime(quote['time'], "%Y-%m-%dT%H:%M:%S")
        pandas_data = quote_time, quote['open'], quote['high'], quote['low'], quote['close'], quote['volume']
        ohlc.append(pandas_data)

    if (len(ohlc)): 
        df = pd.DataFrame(ohlc)
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df.set_index(pd.DatetimeIndex(df['Date']))

        ohlc_dict = {
            'Open':'first',
            'High':'max',
            'Low':'min',
            'Close':'last',
            'Volume':'sum'
        }
        df = df.resample(settings['timesalesBinning']).agg(ohlc_dict)

        # drop resampled data that is outside of market hours. 
        for index, row in df.iterrows():
            hours = index.to_pydatetime().hour
            minutes = index.to_pydatetime().minute
            day_num = index.to_pydatetime().weekday()

            if (day_num > 4): # weekend
                df.drop(index, inplace=True)
            elif (hours >= 16):
                df.drop(index, inplace=True)
            elif (hours == 9 and minutes < 30):
                df.drop(index, inplace=True)
            elif (hours < 9):
                df.drop(index, inplace=True)
            
                
        if (settings['shouldPrintData']):
            pd.set_option('display.max_rows', None)
            print(df)
        
        s  = mpf.make_mpf_style(base_mpf_style='yahoo', 
                                rc={'font.size':10,
                                    'font.weight':'light',
                                    'axes.edgecolor':'black',
                                    'figure.figsize':(8.0, 4.8)
                                    }, 
                                y_on_right=False,
                                facecolor='w',
                                gridstyle=settings['gridstyle']
                                )
        
        
        kwargs = dict(type='candle',volume=True)  
        mpf.plot(df, **kwargs, style=s, 
                title=dict(title="\n\n" + data_title, weight='regular', size=11),               
                datetime_format=' %m/%d %H:%M',
                tight_layout=settings['tight_layout'],
                block=True,
                ylabel="Option Price ($)")        
        # Note: (show_nontrading = False) didn't work, had to custom resample and drop.
    else:
        print("No option trades during period.")
    return
