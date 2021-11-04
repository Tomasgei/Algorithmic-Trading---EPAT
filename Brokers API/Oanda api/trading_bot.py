from oanda_api import OandaAPI

api =OandaAPI()


position_limit = 5
while True:
    command = input("enter command:")
    if command == "T":
        open_pos,pos_list = api.GetOpenPositions()
        if open_pos < position_limit:
            #get trading symbol, calculate position size based on risk
            order = api.PlaceTrade("WTICO_USD",1000)
            print( str(order) )
        else:
            print("Max open positions limit reached!")
    if command == "Q":
        #order = api.PlaceTrade("EUR_USD",-1000)
        print("Quit a trade")
        break