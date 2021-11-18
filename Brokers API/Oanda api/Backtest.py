from typing_extensions import ParamSpec
import pandas as pd
import utils
import instruments
import Backtest_results
pd.set_option("display.max_columns",None)

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
    """
    This function returns MA period in Df column
    """
    return f"MA_{ma}"

def CalculateResults( symbol_info, mashort, malong, price_data):
    price_data["DIFF"] = price_data[GetMaCol(mashort)] - price_data[GetMaCol(malong)] # Get the MA difference for crossover signal
    price_data["DIFF_PREV"] = price_data.DIFF.shift(1) # 
    price_data["TRADE_SIGNAL"] = price_data.apply(TradeSignal, axis=1) # Apply function TradeSignal to DataFrame column
    df_trades = price_data[price_data.TRADE_SIGNAL!=0].copy()
    df_trades["DELTA"] = ( df_trades.mid_c.diff() / symbol_info.pipLocation).shift(-1)
    df_trades["GAIN"] = df_trades["DELTA"]*df_trades["TRADE_SIGNAL"]

    print(f"{symbol_info.name} {mashort} {malong} trades: {df_trades.shape[0]} gain:{df_trades.GAIN.sum():.0f}")
    return Backtest_results.MAResult(
        df_trades= df_trades,
        symbol= symbol_info.name ,
        params={"MaShort": mashort, "MaLong":malong}
    )


def GetHistoricalData(symbol,granularity ):
    """
    This function returns historical data needed for backtest
    """
    df = pd.read_csv(utils.get_his_data_filename(symbol ,granularity))
    non_cols = ["time","volume"]
    mod_cols = [x for x in df.columns if x not in non_cols]
    df[mod_cols] = df[mod_cols].apply(pd.to_numeric)

    return df[["time","mid_c"]]

def ProcessData(ma_short,ma_long,price_data):
    """
    Calculate Moving Avarages, get unique values and add to DataFrame
    """
    ma_list = set(ma_short + ma_long)
    for ma in ma_list:
        price_data[GetMaCol(ma)] = price_data.mid_c.rolling(window=ma).mean()
    
    return price_data

def ProcessResults(results):
    results_list = [r.result_ob() for r in results]
    final_df = pd.DataFrame(results_list)
    print(final_df.info())
    print(final_df.head())


def BackTest():
    """
    comment
    """
    symbol ="SPX500_USD"
    granularity = "H1"
    ma_short = [5,13,18,21,34]
    ma_long = [45,77,100,120,252]
    symbol_info = instruments.Instrument.Get_Istruments_Dict()[symbol] # Get instrument specification
    price_data = GetHistoricalData(symbol, granularity)


    price_data = ProcessData(ma_short,  ma_long, price_data)

    results = []

    for _malong in ma_long:
        for _mashort in ma_short:
            if _mashort >= _malong:
                continue
            results.append( CalculateResults( symbol_info, _mashort, _malong, price_data.copy()))

    ProcessResults(results)


if __name__ == "__main__":
    BackTest()
