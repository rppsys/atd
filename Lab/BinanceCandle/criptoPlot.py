# plotAPIs

# Esse converteu as datas corretamente
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import apiBINANCE as apiBNCE
from datetime import datetime
from math import pi
from bokeh.plotting import figure, show, output_file, output_notebook
from bokeh.models import Toggle, BoxAnnotation, CustomJS, PrintfTickFormatter, ColumnDataSource, Range1d, LabelSet, Label, DatetimeTickFormatter, HoverTool
from bokeh.layouts import column

def plotBNCEMarketHTML(strMarket='ETHBTC',strTime='1d',numData=500,htmlFilename=''):
    df,lst = apiBNCE.getKlines(strMarket,strTime,numData)
    # Convertes colunas numéricas para tipo numérico
    df['open'] = pd.to_numeric(df['open'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['close'] = pd.to_numeric(df['close'])
    df['volume'] = pd.to_numeric(df['volume'])
    df['Quote asset volume'] = pd.to_numeric(df['Quote asset volume'])
    df['Taker buy base asset volume'] = pd.to_numeric(df['Taker buy base asset volume'])
    df['Taker buy quote asset volume'] = pd.to_numeric(df['Taker buy quote asset volume'])
    df['Ignore'] = pd.to_numeric(df['Ignore'])
    # Converte colunas datetime para tipo numérico
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    df['date'] = df['Close time']
    #http://www.learndatasci.com/python-finance-part-3-moving-average-trading-strategy/
    df['SMA21'] = df.close.rolling(window=21).mean()
    df['SMA50'] = df.close.rolling(window=50).mean()
    df['SMA200'] = df.close.rolling(window=200).mean()
    df['EMA8'] = df.close.ewm(span=8,adjust=False).mean()
    df['EMA35'] = df.close.ewm(span=35,adjust=False).mean()

    srLen = int(len(df.close)/10)
    df['SUPORT'] = df.high.rolling(window=srLen).min()
    df['RESIST'] = df.low.rolling(window=srLen).max()

    # Gráficos Estocásticos
    #https://www.investopedia.com/terms/s/stochasticoscillator.asp
    sto_K_param_P = 14
    df['sto_LPclose'] = df.close.rolling(window = sto_K_param_P).min()
    df['sto_LP'] = df.low.rolling(window = sto_K_param_P).min()
    df['sto_HP'] = df.high.rolling(window = sto_K_param_P).max()

    df['sto_K'] = 100*((df['close'] - df['sto_LPclose'])/(df['sto_HP'] - df['sto_LP']))
    df['sto_D'] = df.sto_K.rolling(window=3).mean()

    # Gráficos de Candlestick
    inc = df.close > df.open
    dec = df.open > df.close
    df['date_inc'] = df.date[inc]
    df['date_dec'] = df.date[dec]
    df['open_inc'] = df.open[inc]
    df['open_dec'] = df.open[dec]
    df['close_inc'] = df.close[inc]
    df['close_dec'] = df.close[dec]

    # Parâmetro W
    if strTime == '1m':
        w = 1*60*1000
    elif strTime =='3m':
        w = 3*60*1000
    elif strTime =='5m':
        w = 5*60*1000
    elif strTime =='15m':
        w = 15*60*1000
    elif strTime =='30m':
        w = 30*60*1000
    elif strTime =='1h':
        w = 1*60*60*1000
    elif strTime =='2h':
        w = 2*60*60*1000
    elif strTime =='4h':
        w = 4*60*60*1000
    elif strTime =='6h':
        w = 6*60*60*1000
    elif strTime =='8h':
        w = 8*60*60*1000
    elif strTime =='12h':
        w = 12*60*60*1000
    elif strTime =='1d':
        w = 1*24*60*60*1000
    elif strTime =='3d':
        w = 3*24*60*60*1000
    elif strTime =='1w':
        w = 7*24*60*60*1000
    elif strTime =='1M':
        w = 30*24*60*60*1000

    # Plotagem
    source = ColumnDataSource(df)

    hover = HoverTool(
        tooltips=[
            ("Indice", "$index"),
            ("Valor", "@close{0.000}"),
            ("Data", "@date"),
            ("Volume", "@volume"),
            ("Open time","@{Open time}")
        ],
        formatters={
            'Valor' : 'printf',
            'Data'  : 'datetime',
            'Volume': 'printf',
            'Open time': 'datetime',
        },
        mode='mouse'
    )

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,crosshair"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1500, plot_height=500)
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3
    p.add_tools(hover)

    # Gráfico de Candlestick
    plot_candleHL = p.segment(x0='date', y0='high', x1='date', y1 = 'low', color="red",legend='HL',source=source)
    plot_candleGreen = p.vbar(x='date_inc', width=w, top='open_inc', bottom='close_inc', fill_color="#31BE3A", line_color="black",legend='G',source=source)
    plot_candleRed = p.vbar(x='date_dec', width=w, top='open_dec', bottom='close_dec', fill_color="#F2583E", line_color="black",legend='R',source=source)

    # Gráficos Lineares
    plot_closingPrice = p.line(x = 'date',y='close',line_color="black",line_width=2,line_alpha=0.8,line_dash='solid',legend="Close Price",muted_color='blue', muted_alpha=0.2, source=source)

    # Médias Móveis
    plot_SMA21 = p.line(x = 'date',y = 'SMA21',line_color="gray",line_width=2,line_alpha=0.8,line_dash='dashed',legend="SMA 21",muted_color='gray', muted_alpha=0.1, source=source)
    plot_SMA50 = p.line(x = 'date',y = 'SMA50',line_color="blue",line_width=2,line_alpha=0.8,line_dash='dashed',legend="SMA 50",muted_color='gray', muted_alpha=0.1, source=source)
    plot_SMA200 = p.line(x = 'date',y = 'SMA200',line_color="red",line_width=2,line_alpha=0.8,line_dash='dashed',legend="SMA 200",muted_color='gray', muted_alpha=0.1, source=source)
    plot_EMA8 = p.line(x = 'date',y = 'EMA8',line_color="orange",line_width=2,line_alpha=0.8,line_dash='dashed',legend="EMA 8",muted_color='gray', muted_alpha=0.1, source=source)
    plot_EMA35 = p.line(x = 'date',y = 'EMA35',line_color="purple",line_width=2,line_alpha=0.8,line_dash='dashed',legend="EMA 35",muted_color='gray', muted_alpha=0.1, source=source)

    # Atributos Gerais de Todos os Gráficos
    p.title.text = strMarket + '-' + strTime + '-' + str(numData)
    if htmlFilename == '':
        htmlFilename = p.title.text + '.html'
    else:
        if htmlFilename.find('.html') < 0:
            htmlFilename = htmlFilename + '.html'

    # Eixo X - Datas
    p.xaxis.axis_label = 'Tempo'
    p.xgrid.grid_line_alpha = 0.6
    p.xgrid.grid_line_dash = [6, 4]

    listAux = ["%d%b/%y-%Hh%Mm"]

    p.xaxis.formatter=DatetimeTickFormatter(
            hours=listAux,
            days=listAux,
            months=listAux,
            years=listAux,
        )

    # Eixo Y - Valores
    p.yaxis.axis_label = 'Preço'
    p.yaxis.minor_tick_in = -3
    p.yaxis.minor_tick_out = 8
    p.yaxis[0].formatter = PrintfTickFormatter(format="%8.8f")

    p.ygrid.band_fill_color="olive"
    p.ygrid.band_fill_alpha = 0.1
    p.ygrid.grid_line_alpha = 0.6
    p.ygrid.grid_line_dash = [6, 4]

    # Legendas
    p.legend.location = "top_right"
    p.legend.click_policy="hide"

    ##############################################
    # Figura para Gráficos Estocásticos
    ##############################################
    q = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1500,x_range=p.x_range, plot_height= int(0.5 * p.plot_height))
    q.xaxis.major_label_orientation = pi/4
    q.grid.grid_line_alpha=0.3
    q.add_tools(hover)

    plot_stoK = q.line(x = 'date',y = 'sto_K',line_color="red",line_width=2,line_alpha=0.8,line_dash='solid',legend="STO K",muted_color='gray', muted_alpha=0.1, source=source)
    plot_stoD = q.line(x = 'date',y = 'sto_D',line_color="blue",line_width=2,line_alpha=0.8,line_dash='solid',legend="STO D",muted_color='gray', muted_alpha=0.1, source=source)

    # Caixas delimitando faixas de oversold e overbought
    low_box = BoxAnnotation(top=20, fill_alpha=0.1, fill_color='red')
    mid_box = BoxAnnotation(bottom=20, top=80, fill_alpha=0.1, fill_color='green')
    high_box = BoxAnnotation(bottom=80, fill_alpha=0.1, fill_color='red')

    q.add_layout(low_box)
    q.add_layout(mid_box)
    q.add_layout(high_box)

    # Eixo X - Datas
    q.xaxis.axis_label = 'Tempo'
    q.xgrid.grid_line_alpha = 0.6
    q.xgrid.grid_line_dash = [6, 4]

    listAux = ["%d%b/%y-%Hh%Mm"]

    q.xaxis.formatter=DatetimeTickFormatter(
            hours=listAux,
            days=listAux,
            months=listAux,
            years=listAux,
        )

    # Eixo Y - Valores
    q.yaxis.axis_label = 'Porcentagem'
    q.yaxis.minor_tick_in = -3
    q.yaxis.minor_tick_out = 8
    q.yaxis[0].formatter = PrintfTickFormatter(format="%8.8f")

    q.ygrid.band_fill_color="olive"
    q.ygrid.band_fill_alpha = 0.1
    q.ygrid.grid_line_alpha = 0.6
    q.ygrid.grid_line_dash = [6, 4]

    # Legendas
    q.legend.location = "top_right"
    q.legend.click_policy="hide"

    output_file(htmlFilename, title=p.title.text)
    show(column(p,q))

def plotBNCEMarketHTML3(strMarket='ETHBTC',strTime='1d',numData=500,htmlFilename=''):
    df,lst = apiBNCE.getKlines(strMarket,strTime,numData)
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    df['date'] = df['Close time']

    #http://www.learndatasci.com/python-finance-part-3-moving-average-trading-strategy/
    df['SMA21'] = df.close.rolling(window=21).mean()
    df['SMA50'] = df.close.rolling(window=50).mean()
    df['SMA200'] = df.close.rolling(window=200).mean()
    df['EMA8'] = df.close.ewm(span=8,adjust=False).mean()
    df['EMA35'] = df.close.ewm(span=35,adjust=False).mean()

    srLen = int(len(df.close)/10)
    df['SUPORT'] = df.high.rolling(window=srLen).min()
    df['RESIST'] = df.low.rolling(window=srLen).max()

    # Gráficos de Candlestick
    inc = df.close > df.open
    dec = df.open > df.close
    df['date_inc'] = df.date[inc]
    df['date_dec'] = df.date[dec]
    df['open_inc'] = df.open[inc]
    df['open_dec'] = df.open[dec]
    df['close_inc'] = df.close[inc]
    df['close_dec'] = df.close[dec]

    # Parâmetro W
    if strTime == '1m':
        w = 1*60*1000
    elif strTime =='3m':
        w = 3*60*1000
    elif strTime =='5m':
        w = 5*60*1000
    elif strTime =='15m':
        w = 15*60*1000
    elif strTime =='30m':
        w = 30*60*1000
    elif strTime =='1h':
        w = 1*60*60*1000
    elif strTime =='2h':
        w = 2*60*60*1000
    elif strTime =='4h':
        w = 4*60*60*1000
    elif strTime =='6h':
        w = 6*60*60*1000
    elif strTime =='8h':
        w = 8*60*60*1000
    elif strTime =='12h':
        w = 12*60*60*1000
    elif strTime =='1d':
        w = 1*24*60*60*1000
    elif strTime =='3d':
        w = 3*24*60*60*1000
    elif strTime =='1w':
        w = 7*24*60*60*1000
    elif strTime =='1M':
        w = 30*24*60*60*1000

    # Plotagem
    source = ColumnDataSource(df)

    hover = HoverTool(
        tooltips=[
            ("Indice", "$index"),
            ("Valor", "@close{0.000}"),
            ("Data", "@date"),
            ("Volume", "@volume"),
            ("Open time","@{Open time}")
        ],
        formatters={
            'Valor' : 'printf',
            'Data'  : 'datetime',
            'Volume': 'printf',
            'Open time': 'datetime',
        },
        mode='mouse'
    )

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,crosshair"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1500)
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3
    p.add_tools(hover)

    # Gráfico de Candlestick
    plot_candleHL = p.segment(x0='date', y0='high', x1='date', y1 = 'low', color="red",legend='HL',source=source)
    plot_candleGreen = p.vbar(x='date_inc', width=w, top='open_inc', bottom='close_inc', fill_color="#31BE3A", line_color="black",legend='G',source=source)
    plot_candleRed = p.vbar(x='date_dec', width=w, top='open_dec', bottom='close_dec', fill_color="#F2583E", line_color="black",legend='R',source=source)


    # Gráficos Lineares
    plot_closingPrice = p.line(x = 'date',y='close',line_color="black",line_width=2,line_alpha=0.8,line_dash='solid',legend="Close Price",muted_color='blue', muted_alpha=0.2, source=source)

    # Médias Móveis
    plot_SMA21 = p.line(x = 'date',y = 'SMA21',line_color="gray",line_width=2,line_alpha=0.8,line_dash='dashed',legend="SMA 21",muted_color='gray', muted_alpha=0.1, source=source)
    plot_SMA50 = p.line(x = 'date',y = 'SMA50',line_color="blue",line_width=2,line_alpha=0.8,line_dash='dashed',legend="SMA 50",muted_color='gray', muted_alpha=0.1, source=source)
    plot_SMA200 = p.line(x = 'date',y = 'SMA200',line_color="red",line_width=2,line_alpha=0.8,line_dash='dashed',legend="SMA 200",muted_color='gray', muted_alpha=0.1, source=source)
    plot_EMA8 = p.line(x = 'date',y = 'EMA8',line_color="orange",line_width=2,line_alpha=0.8,line_dash='dashed',legend="EMA 8",muted_color='gray', muted_alpha=0.1, source=source)
    plot_EMA35 = p.line(x = 'date',y = 'EMA35',line_color="purple",line_width=2,line_alpha=0.8,line_dash='dashed',legend="EMA 35",muted_color='gray', muted_alpha=0.1, source=source)


    # Atributos Gerais de Todos os Gráficos
    p.title.text = strMarket + '-' + strTime + '-' + str(numData)
    if htmlFilename == '':
        htmlFilename = p.title.text + '.html'
    else:
        if htmlFilename.find('.html') < 0:
            htmlFilename = htmlFilename + '.html'


    # Eixo X - Datas
    p.xaxis.axis_label = 'Tempo'
    p.xgrid.grid_line_alpha = 0.6
    p.xgrid.grid_line_dash = [6, 4]

    listAux = ["%d%b/%y-%Hh%Mm"]

    p.xaxis.formatter=DatetimeTickFormatter(
            hours=listAux,
            days=listAux,
            months=listAux,
            years=listAux,
        )

    # Eixo Y - Valores
    p.yaxis.axis_label = 'Preço'
    p.yaxis.minor_tick_in = -3
    p.yaxis.minor_tick_out = 8
    p.yaxis[0].formatter = PrintfTickFormatter(format="%8.8f")

    p.ygrid.band_fill_color="olive"
    p.ygrid.band_fill_alpha = 0.1
    p.ygrid.grid_line_alpha = 0.6
    p.ygrid.grid_line_dash = [6, 4]

    # Legendas
    p.legend.location = "top_right"
    p.legend.click_policy="hide"

    output_file(htmlFilename, title=p.title.text)
    show(p)
    return df


def plotBNCEMarketHTML2(strMarket='ETHBTC',strTime='1d',numData=500):
    df,lst = apiBNCE.getKlines(strMarket,strTime,numData)
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    df['date'] = df['Open time']

    inc = df.close > df.open
    dec = df.open > df.close
    w = 2*12*60*60*1000 # half day in ms

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover,crosshair"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1500)
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3

    p.segment(df.date, df.high, df.date, df.low, color="red")
    p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="#31BE3A", line_color="black")
    p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

    # Aqui eu poderia plotar linhas de suporte, media móvel etc
    p.line(df.date,float(df.high.median()))
    p.line(df.date,float(df.low.median()))

    # NEW: customize by setting attributes
    p.title.text = strMarket + '-' + strTime + '-' + str(numData)
    p.legend.location = "top_left"
    p.grid.grid_line_alpha=0
    p.xaxis.axis_label = 'Tempo'
    p.yaxis.axis_label = 'Preço'
    p.ygrid.band_fill_color="olive"
    p.ygrid.band_fill_alpha = 0.1
    output_file(p.title.text + ".html", title=p.title.text)
    show(p)  # open a browser
