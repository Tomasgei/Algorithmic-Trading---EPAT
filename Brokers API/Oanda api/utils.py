import datetime as dt
from dateutil.parser import *

def get_his_data_filename(symbol, granularity):
    return f"historical_data/{symbol}_{granularity}.csv"

def get_instruments_data_filename():
    return "Oanda_instrument_list.csv"

def time_utc():
    return dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)

def get_utc_dt_from_string(data_str):
    d = parse(data_str)
    return d.replace(tzinfo=dt.timezone.utc)



if __name__ == "__main__":
    print(dt.datetime.utcnow())
    print(time_utc())
    print(get_utc_dt_from_string("2021-01-05 05:30:21"))
