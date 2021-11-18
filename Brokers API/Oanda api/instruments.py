import pandas as pd
import utils

"""
This script managing trading instruments data to download and save it to the file
by collect_hi_data.py
"""


class Instrument():
    def __init__(self,ob):
        self.name = ob["name"]
        self.ins_type = ob["type"]
        self.displayName = ob["displayName"]
        self.pipLocation = pow(10,ob["pipLocation"])
        self.marginRate = ob["marginRate"]
    
    def __repr__(self):
        return str(vars(self))

    @classmethod
    def Get_Instruments_Df(cls):
        """
        This function gets DataFrame of all trading instruments
        Returns: DataFrame
        """
        return pd.read_csv(utils.get_instruments_data_filename())
    
    @classmethod
    def Get_Instruments_List(cls):
        """
        This function gets list of all trading instruments 
        from function Get_Instruments_Df()
        Returns: List of Dictionaries
        """
        df = cls.Get_Instruments_Df()
        return [Instrument(x) for x in df.to_dict(orient="records")]

    @classmethod
    def Get_Istruments_Dict(cls):
        """
        This function gets formatted output k,v for every trading instrument
        k = trading symbol, v = instrument specification
        format: EUR_HUF {'name': 'EUR_HUF', 'ins_type': 'CURRENCY', 'displayName': 'EUR/HUF', 'pipLocation': 0.01, 'marginRate': 0.05}
        """
        i_list = cls.Get_Instruments_List()
        i_keys = [x.name for x in i_list if x]
        return { k:v for (k,v) in zip(i_keys, i_list) }

    @classmethod
    def Get_Instrument_Symbol(cls,symbol):
        """
        This function gets trading instrument by its trading symbol: 
        example: symbol = EUR_USD
        """
        ticker = cls.Get_Istruments_Dict()
        if symbol in ticker:
            return ticker[symbol]
        else:
            return None

    @classmethod
    def Get_Symbols_From_String(cls,symbol):
        """
        Input string example: "GBP,EUR,USD,CAD,JPY,NZD,CHF,SPX500,DE30,US2000"
        This function gets tickers strings in format: X_Y for all combinations
        and query if trading symbol exist in Get_Istruments_Dict() 
        """
        existing_pairs = cls.Get_Istruments_Dict().keys()
        symbols = symbol.split(',')

        symbol_list = []
        for s1 in symbols:
            for s2 in symbols:
                s = f"{s1}_{s2}"
                if s in existing_pairs:
                    symbol_list.append(s)
        return symbol_list

if __name__ == "__main__":
    print(Instrument.Get_Instrument_Symbol("EUR_USD"))