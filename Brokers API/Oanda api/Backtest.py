from typing_extensions import ParamSpec
import pandas as pd
import utils
import instruments

def TradeSignal(row):
    """
    This function returns trade signal FLAG in DataFrame
    """
    if row.DIFF >= 0 and row.DIFF_PREV < 0:
        return 1 
    if row.DIFF <= 0 and row.DIFF_PREV >0:
        return -1
    return 0

def GetMaCol(ma):
    return f"MA_{ma}"

def GetHistoricalData(symbol,granularity ):
    """
    comment
    """
    df = pd.read_csv(utils.get_his_data_filename(symbol ,granularity))
    non_cols = ["time","volume"]
    mod_cols = [x for x in df.columns if x not in non_cols]
    df[mod_cols] = df[mod_cols].apply(pd.to_numeric)

    return df[["time","mid_c"]]

def ProcessData(ma_short,ma_long,price_data):
    """
    comment
    """
    ma_list = set(ma_short + ma_long)
    for ma in ma_list:
        price_data[GetMaCol(ma)] = price_data.mid_c.rolling(window=ma).mean()
    
    return price_data

def BackTest():
    """
    comment
    """
    symbol ="SPX500_USD"
    granularity = "H1"
    ma_short = [5,13,18,21,34,45,55]
    ma_long = [13,21,45,77,100,120,252]
    i_pair = instruments.Instrument.GetIstrumentsDict()[symbol] # Get instrument specification

    price_data = GetHistoricalData(symbol, granularity)
    price_data = ProcessData(ma_short,  ma_long, price_data)
    print(price_data.tail())

if __name__ == "__main__":
    BackTest()
