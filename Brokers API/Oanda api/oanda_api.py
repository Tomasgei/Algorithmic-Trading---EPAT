import requests
import pandas as pd
import utils
import json
import configparser  
config = configparser.ConfigParser() 
config.read("C:/Users/tomas/Dropbox/Prop-Trading Business/oanda.cfg") 


"""
This script is API client 
"""



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


    def Get_Account(self):
        """
        Function type: Api Data Request
        Get the full details for a single Account that client has access to.
        Full pending Order, open Trade and open Position representations are provided
        """
        url = "/v3/accounts/"
        try:
            response = self.session.get(f"{self.oanda_api_url}/v3/accounts/"+self.account_id,headers=self.headers)
            data = response.json()
        except:
            print(f"Error wit getting account {self.account_id}"+response.status_code)
        return response.status_code, data
    
    def Get_Account_Balance(self):
        """
        Function type: Api Data Request
        Get last account balance level
        Returns: float
        """
        response = self.Get_Account()
        code, data = response
        if code == 200:
            balance = data["account"]["balance"]
            return float(balance)
        else:
            return None

    def Get_Account_Margin_Used(self):
        """
        Function type: Api Data Request
        Get level of margin used to maintain all positions
        Returns: float
        """
        response = self.Get_Account()
        code, data = response
        if code == 200:
            margin = data["account"]["marginUsed"]
            return float(margin)
        else:
            return None

    def Get_Account_Margin_Available(self):
        """
        Function type: Api Data Request
        Get level of margin available to open new positions
        Returns: float
        """
        response = self.Get_Account()
        code, data = response
        if code == 200:
            margin = data["account"]["marginAvailable"]
            return float(margin)
        else:
            return None


    def Get_All_Instruments(self):
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

    def Get_Instruments_DataFrame(self):
        """
        Function type: Data Manipulation
        Get DataFrame of trading instruments.
        """
        code, data = self.Get_All_Instruments()
        if code == 200:
            df =pd.DataFrame(data["instruments"])
            return df[["name","type","displayName","pipLocation","marginRate"]]
        else:
            return None

    def Save_Instruments(self):
        """
        Function type: Data Manipulation
        Save list of instruments to .csv
        """
        df = self.Get_Instruments_DataFrame()
        if df is not None:
            df.to_csv(utils.get_instruments_data_filename())

    def Get_Candle_Data(self, symbol, granularity="H1", count=None, start=None, end=None ):
        """
        Function type: Api Data Request
        Fetch candlestick data for an instrument
        """
        url = f"{self.oanda_api_url}/v3/instruments/"+symbol+"/candles"
        params={
            "granularity":granularity,
            "price":"MBA",
            "count":count 
        }

        if start is not None and end is not None:
            params["from"]  = int(start.timestamp())
            params["to"]    = int(end.timestamp())
        elif count is not None:
            params["count"] = count
        else:
            params["count"] = 4000
    
        response = self.session.get(url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            return response.status_code,None

        return response.status_code, response.json()
    

    def Get_Open_Positions(self):
        """
        Function type: Api Data Request
        This function gets count number of all open positions on account 
        and list of dictionaries in format: 
        {"instrument":"EUR_USD","longUnits":"10000",shortUnits":"10000"}
        Returns: Integer, List of dict 
        """
        url = f"{self.oanda_api_url}/v3/accounts/"+self.account_id+"/openPositions"
        try:
            response = self.session.get(url,headers=self.headers)
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
        url = f"{self.oanda_api_url}/v3/accounts/"+self.account_id+"/orders"
        data = {
            "order": {
            "units": units,
            "instrument": symbol,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
            }
        }
        response = self.session.post(url ,headers=self.headers, json=data)
        json_data = response.json()

        order_id = 0
        trade_id = 0

        if 'orderFillTransaction' in json_data.keys() and 'tradeOpened' in json_data['orderFillTransaction'].keys():
            return int(json_data['orderFillTransaction']['tradeOpened']['tradeID'])
        
        return None



if __name__ == '__main__':
    api=OandaAPI()
    print(api.Get_Account_Margin_Used())
    print(api.Get_Account_Balance())
    print(api.Get_Open_Positions())

    start = utils.get_utc_dt_from_string("2016-02-03 15:00:00")
    end = utils.get_utc_dt_from_string("2016-02-07 15:00:00")
    print(api.Get_Candle_Data("EUR_NOK", granularity="H1", start=start, end=end ))
 


