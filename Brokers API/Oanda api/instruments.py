import pandas as pd
import utils

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
    def GetInstrumentsDf(cls):
        """
        This function gets DataFrame of all trading instruments
        Returns: DataFrame
        """
        return pd.read_csv(utils.get_instruments_data_filename())
    
    @classmethod
    def GetInstrumentsList(cls):
        """
        This function gets list of all trading instruments 
        from function GetInstrumentsDf()
        Returns: List of Dictionaries
        """
        df = cls.GetInstrumentsDf()
        return [Instrument(x) for x in df.to_dict(orient="records")]

    @classmethod
    def GetIstrumentsDict(cls):
        """
        This function gets formatted output k,v for every trading instrument
        k = trading symbol, v = instrument specification
        format: EUR_HUF {'name': 'EUR_HUF', 'ins_type': 'CURRENCY', 'displayName': 'EUR/HUF', 'pipLocation': 0.01, 'marginRate': 0.05}
        """
        i_list = cls.GetInstrumentsList()
        i_keys = [x.name for x in i_list if x]
        return { k:v for (k,v) in zip(i_keys, i_list) }

    @classmethod
    def GetInstrumentSymbol(cls,symbol):
        """
        This function gets trading instrument by its trading symbol: 
        example: symbol = EUR_USD
        """
        ticker = cls.GetIstrumentsDict()
        if symbol in ticker:
            return ticker[symbol]
        else:
            return None

if __name__ == "__main__":
    print(Instrument.GetInstrumentSymbol("EUR_USD"))