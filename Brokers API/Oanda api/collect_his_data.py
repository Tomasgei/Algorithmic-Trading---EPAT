import pandas as pd
import datetime as dt

# get info for available trading instruments and their specifications
from instruments import Instrument 
# get utils functions 
import utils
# get api client
from oanda_api import OandaAPI


"""
This script managing trading instruments data to download and save it to the file

"""


INCREMENTS = {
    #"M1" : 1,
    #"M5" : 5,
    #"M10" : 10,
    "M15" : 15,
    #"M30" : 30,
    #"H1" : 60,
    #"H4" : 240,
}

def Get_Candles_DataFrame(json_response):
    """
    This function creates Dataframe from data
    aquired by function Get_Candle_Data() 
    """
    prices = ["mid", "bid", "ask"]
    ohlc = ["o","h","l","c"]
    our_data = []
    for candle in json_response["candles"]:
        if candle["complete"] == False:
            continue
        new_dict = {}
        new_dict["time"] = candle["time"]
        new_dict["volume"] = candle["volume"]
        for price in prices:
            for oh in ohlc:
                new_dict[f"{price}_{oh}"] = candle[price][oh]
        our_data.append(new_dict)
    candles_df = pd.DataFrame(our_data)
    return candles_df

def create_file(symbol, granularity, api, starting_date, ending_date):
    """
    This function creates increment steps -> candle_count to download longer history 
    of intraday data for instrument, because count limit = 5000
    and save to file 
    """
    candle_count = 2000
    time_step =INCREMENTS[granularity] * candle_count
    end_date = utils.get_utc_dt_from_string(ending_date)
    date_from = utils.get_utc_dt_from_string(starting_date)
    candle_dfs = []
    end = date_from
    while end < end_date:
        end = date_from + dt.timedelta(minutes=time_step)
        print(date_from, end)
        if end > end_date:
            end = end_date

        code, json_data = api.Get_Candle_Data(symbol,granularity=granularity,start=date_from, end=end )
        if code == 200 and len(json_data["candles"]) > 0:
            candle_dfs.append(Get_Candles_DataFrame(json_data))
        elif code != 200:
            print("ERROR", symbol,granularity,date_from,end)
            break
        date_from = end

    final_df = pd.concat(candle_dfs)
    final_df.drop_duplicates(subset="time", inplace=True)
    final_df.sort_values(by="time", inplace=True)
    final_df.to_csv(utils.get_his_data_filename(symbol,granularity))
    print(f"{symbol} {granularity} {final_df.iloc[0].time} {final_df.iloc[-1].time}")


def run_collection(start = "2016-01-01 00:00:00", end = "2019-11-01 00:00:00"):
    """
    This function downloads historical data based on symbols in symbol_list/ on symbol string 
    and save them to separeta file for each symbol for backtesting ana analysis
    history lenght settings = start = "2018-01-01 00:00:00" end = "2020-12-31 23:59:59" 
    """
    symbol_list = "GBP,EUR,USD,CAD,JPY,NZD,CHF,SPX500,DE30,US2000"
    api = OandaAPI()
    for g in INCREMENTS.keys():
        for i in Instrument.Get_Symbols_From_String(symbol_list):
            print(g,i)
            create_file(i,g,api,start,end)

if __name__ == '__main__':
    run_collection()
 