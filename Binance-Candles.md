# Candlestick da Binance com Gráficos de Média

Acesse:

https://github.com/rppsys/atd/tree/master/Lab/BinanceCandle

Nessa pasta está o código fonte que criei de uma API capaz de acessar gráficos de cotações
de criptoativos da exchange binance:

https://www.binance.com/en

O arquivo **apiBINANCE.py** é responsável por acessar a API da Binance e puxar os dados;

O arquivo **criptoPLOT.py** usa a **apiBINANCE.py** para fazer a plotagem dos gráficos de candlestick 
e também de algumas médias móveis.

O arquivo **Candlestick.ipynb** é um jupyter-notebook que mostra como usar os arquivos acima descritos.

    import criptoPlot as cp
    import apiBINANCE as apiBNCE
    
    df = cp.plotBNCEMarketHTML('BTCUSDT')
    
 Ao executar esses comandos ele vai plotar os candleticks do par bitcoin e dolar *BTCUSDT* e também já vai 
 traçar diversas médias móveis. 
 
 Veja o código para entender como isso é feito.
 
 ##### Voltar para a página inicial em: 
 
 https://github.com/rppsys/atd/  