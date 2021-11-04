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
    def get_instrument_df(cls):
        return pd.read_csv(utils.get_instruments_data_filename())
    
    @classmethod
    def get_instruments_list(cls):
        df = cls.get_instrument_df()
        return [Instrument(x) for x in df.to_dict(orient="records")]


if __name__ == "__main__":
    print(Instrument.get_instrument_df())