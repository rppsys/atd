from urllib.request import Request, urlopen
import numpy as np
import pandas as pd
import datetime
import json
import math

# Ver https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
siteApi = 'https://api.binance.com'

"""
Método getData usado para fazer o pedido e transformar os dados recebidos
em formato python
"""
def getData(method='api/v1/time'):
    "Get data of method"
    req = Request(siteApi + '/' + method, headers={'User-Agent': 'Mozilla/5.0'})
    JSON = urlopen(req).read()
    return json.loads(JSON)


# Esse deu certo, vou deixar anotado ui:
#Vou precisa quando eu quiser plotar gráficos de candlestick
#https://api.binance.com/api/v1/klines?symbol=LTCBTC&interval=1d

# Aqui vem so o price
#GET /api/v3/ticker/price

#GET /api/v1/ticker/24hr

def public_getMarketSummaries():
    dt = getData('api/v1/ticker/24hr')
    df = pd.DataFrame(dt)
    lst = list(df.columns.values)
    return df,lst
MarketSummaries_DataframeData, MarketSummaries_ParamList = public_getMarketSummaries()

def listMarketThatContainsStr(strContent=''):
    df = MarketSummaries_DataframeData
    return df[df['symbol'].str.contains(strContent)]['symbol']

def getCoinValueByParam(coin='LTC',param='lastPrice'):
    strMarket =  coin + 'BTC'
    df = MarketSummaries_DataframeData
    return df[df['symbol']==strMarket][param].values[0]


'''
[
  [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore
  ]
]

Kline/Candlestick chart intervals:

m -> minutes; h -> hours; d -> days; w -> weeks; M -> months

    1m
    3m
    5m
    15m
    30m
    1h
    2h
    4h
    6h
    8h
    12h
    1d
    3d
    1w
    1M
'''

#https://stackoverflow.com/questions/9539921/how-do-i-create-a-python-function-with-optional-arguments
#https://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_datetime.html
#http://avilpage.com/2014/11/python-unix-timestamp-utc-and-their.html
#https://www.freeformatter.com/epoch-timestamp-to-date-converter.html

Klines_Colunas = ['Open time','open','high','low','close','volume','Close time','Quote asset volume','Number of trades','Taker buy base asset volume','Taker buy quote asset volume','Ignore']
def getKlines(symbol='LTCBTC',interval='1d',limit=500):
    dt = getData('api/v1/klines?symbol=' + symbol + '&interval=' + interval + '&limit=' + str(limit))
    df = pd.DataFrame(dt,columns=Klines_Colunas)
    lst = list(df.columns.values)
    return df,lst
Klines_DataframeData, Klines_ParamList = getKlines()

#Tentar por Aqui
#https://plot.ly/pandas/candlestick-charts/
