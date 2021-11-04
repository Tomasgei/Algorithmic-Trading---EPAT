import requests
import pandas as pd
import utils
import json
import configparser  
config = configparser.ConfigParser() 
config.read("C:/Users/tomas/Dropbox/Prop-Trading Business/oanda.cfg") 

class OandaAPI():
    """
    Initialize Oanda api connection 
    """
    def __init__(self):
        self.session         = requests.Session() #Estabilish HTTP Persistent Connection - Keep-Alive
        self.api_key         =  config["oanda"]['api_key'] # Enter Your api key
        self.oanda_api_url   =  config["oanda"]['oanda_api_url'] # Enter api url
        self.account_id      =  config["oanda"]['account_id'] # Enter your account id
        self.headers         = {'Authorization': f'Bearer {self.api_key}',"Content-Type": "application/json"} # authetication header for secure api requests

    def GetAccount(self):
        """
        Function type: Api Data Request
        Get the full details for a single Account that client has access to.
        Full pending Order, open Trade and open Position representations are provided
        """
        try:
            response = self.session.get(f"{self.oanda_api_url}/v3/accounts/"+self.account_id,headers=self.headers)
            data = response.json()
        except:
            print(f"Error wit getting account {self.account_id}"+response.status_code)
        return response.status_code, data
    
    def GetAccountBalance(self):
        """
        Function type: Api Data Request
        Get last account balance level
        Returns: float
        """
        response = self.GetAccount()
        code, data = response
        if code == 200:
            balance = data["account"]["balance"]
            return float(balance)
        else:
            return None

    def GetAccountMarginUsed(self):
        """
        Function type: Api Data Request
        Get level of margin used to maintain all positions
        Returns: float
        """
        response = self.GetAccount()
        code, data = response
        if code == 200:
            margin = data["account"]["marginUsed"]
            return float(margin)
        else:
            return None

    def GetAccountMarginAvailable(self):
        """
        Function type: Api Data Request
        Get level of margin available to open new positions
        Returns: float
        """
        response = self.GetAccount()
        code, data = response
        if code == 200:
            margin = data["account"]["marginAvailable"]
            return float(margin)
        else:
            return None


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

    def GetCandleData(self, symbol, granularity, price, count):
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

    def GetOpenPositions(self):
        """
        Function type: Api Data Request
        This function gets count number of all open positions on account 
        and list of dictionaries in format: 
        {"instrument":"EUR_USD","longUnits":"10000",shortUnits":"10000"}
        Returns: Integer, List of dict 
        """
        try:
            response = self.session.get(f"{self.oanda_api_url}/v3/accounts/"+self.account_id+"/openPositions",headers=self.headers)
            data = response.json()
            openPositions = int(len(data["positions"]))
            if openPositions >0:
                positions_data = []
                for dic in data["positions"]:
                    new_dict = {}
                    new_dict["instrument"] = dic["instrument"]
                    new_dict["longUnits"] = dic["long"]["units"]
                    new_dict["shortUnits"] = dic["short"]["units"]
                    positions_data.append(new_dict)  
            else:
                positions_data = None
        except:
            print(response.status_code)
        return openPositions, positions_data


    def PlaceTrade(self,symbol,units):
        data = {
            "order": {
            "units": units,
            "instrument": symbol,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
            }
        }
        response = self.session.post(f"{self.oanda_api_url}/v3/accounts/"+self.account_id+"/orders",headers=self.headers, json=data)
        json_data = response.json()

        order_id = 0
        trade_id = 0

        if 'orderFillTransaction' in json_data.keys() and 'tradeOpened' in json_data['orderFillTransaction'].keys():
            return int(json_data['orderFillTransaction']['tradeOpened']['tradeID'])
        
        return None



if __name__ == '__main__':
    api=OandaAPI()
    print(api.GetAccountMarginUsed())
    print(api.GetAccountBalance())
    print(api.GetOpenPositions())
 


