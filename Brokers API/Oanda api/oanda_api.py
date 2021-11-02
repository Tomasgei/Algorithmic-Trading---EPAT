import requests
import pandas as pd
import utils
import configparser  
config = configparser.ConfigParser() 
config.read("C:/Users/tomas/Dropbox/Prop-Trading Business/oanda.cfg") 




class OandaAPI():

    def __init__(self):
        self.session = requests.Session()
        self.api_key         =  config["oanda"]['api_key']
        self.oanda_api_url   =  config["oanda"]['oanda_api_url']
        self.account_id      =  config["oanda"]['account_id']
        self.headers         = {'Authorization': f'Bearer {self.api_key}'}


    def GetAllInstruments(self):
        """
        Function type: Api Data Request
        Get list of tradable instruments for the given Account.
        """
        try:
            response = self.session.get(f"{self.oanda_api_url}/v3/accounts/"+self.account_id+"/instruments",headers=self.headers)
            data = response.json()
            print(response.status_code)
        except:
            print(response.status_code)
        return response.status_code, data

    def GetInstrumentDataFrame(self):
        """
        Function type: Data Manipulation
        Get DataFrame of trading instruments.
        """
        code, data = self.GetAllInstruments()
        if code == 200:
            df =pd.DataFrame(data["instruments"])
            return df[["name","type","displayName","pipLocation","marginRate"]]
        else:
            return None

    def SaveInstruments(self):
        """
        Function type: Data Manipulation
        Save list of instruments to .csv
        """
        df = self.GetInstrumentDataFrame()
        if df is not None:
            df.to_csv(utils.get_instruments_data_filename())

    def GetCandleData(self, symbol, granularity="H1", price="MBA", count=10):
        """
        Function type: Api Data Request
        Fetch candlestick data for an instrument
        """
        params={
            "granularity":granularity,
            "price":price,
            "count":count 
        }

        try:
            response = self.session.get(f"{self.oanda_api_url}/v3/instruments/"+symbol+"/candles",headers=self.headers, params=params)
            data = response.json()
            print(response.status_code)
        except:
            print(response.status_code)
        return response.status_code, data


if __name__ == '__main__':
    api=OandaAPI()
    df =api.SaveInstruments()
