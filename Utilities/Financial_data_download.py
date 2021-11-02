import pandas as pd
import pandas_datareader as web
from datetime import date

def download_daily_data(symbol):
    """
    The function download daily stock data from Yahoo finance to pandas Dataframe 
    using Pandas_datareader module https://pandas-datareader.readthedocs.io/en/latest/
    between the dates specified.
    """
    start  = input("Start date :"+str())
    end    = input("End date :"+str())
    if end == "":
        today = date.today() 
        end = today.strftime("%d.%m.%Y")

    try: 
        df = web.DataReader(symbol,"yahoo", start=start, end = end)
        print(f"Data for symbol {symbol} was downloaded sucessfully!")
    except:
        print(f"There is some error for symbol {symbol} with data download")
    # save data to csv file    
    df.to_csv(f"{symbol}_{start}-{end}.csv")    
    return df

symbol = input("Tickers to download :"+str())
download_daily_data(symbol)