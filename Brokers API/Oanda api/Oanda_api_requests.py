import requests
my_url = "https://api-fxpractice.oanda.com"
session = requests.Session()

# My functions for api requests
def GetAccount(headers,account_id):
    """
    Get the full details for a single Account that client has access to.
    Full pending Order, open Trade and open Position representations are provided
    """
    try:
        response = session.get(f"{my_url}/v3/accounts/"+account_id,headers=headers)
        data = response.json()
        print(response.status_code)
    except:
        print(response.status_code)
    return data

def GetAccountSummary(headers,account_id):
    """
    Get a summary for single Account that client has access to.
    """
    try:
        response = session.get(f"{my_url}/v3/accounts/"+account_id+"/summary",headers=headers)
        data = response.json()
        print(response.status_code)
    except:
        print(response.status_code)
    return data

def GetAllInstruments(headers,account_id):
    """
    Get list of tradable instruments for the given Account.
    """
    try:
        response = session.get(f"{my_url}/v3/accounts/"+account_id+"/instruments",headers=headers)
        data = response.json()
        print(response.status_code)
    except:
        print(response.status_code)
    return data

def GetInstrument(headers,account_id,symbol):
    """
    Get list of tradable instruments for the given Account.
    """
    try:
        response = session.get(f"{my_url}/v3/accounts/"+account_id+"/instruments",headers=headers,params={"instruments":symbol})
        data = response.json()
        print(response.status_code)
    except:
        print(response.status_code)
    return data

def GetCandleData(headers,symbol,granularity="H1",price="MBA",count=10):
    """
    Fetch candlestick data for an instrument
    """
    try:
        response = session.get(f"{my_url}/v3/instruments/"+symbol+"/candles",headers=headers, params={"granularity":granularity,"price":price,"count":count })
        data = response.json()
        print(response.status_code)
    except:
        print(response.status_code)
    return data