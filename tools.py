import pandas as pd
import yfinance as yf
from langchain.tools import tool

@tool  
def get_recent_news(ticker: str, max_items: int = 5):
    results = yf.Search(ticker).news
    return [{"title": item["title"], "link": item["link"]} 
            for item in results[:max_items]]
     
@tool 
def get_dividend_history(ticker: str): 
    """
    Params: 
        str: ticker corresponsing to the analyzed stock 
    Returns:
        pd.Series with value of the dividend
    """
    return yf.Ticker(ticker).get_dividends(period='10Y')


@tool 
def get_price_trend(ticker: str): 
    """
    Params: 
        str: ticker corresponding to the analyzed stock  
    Returns : 
         pd.DataFrame: dataframe with the following columns ['Open', 'High', 
         'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
    """
    return yf.Ticker(ticker).history(period="1Y") 


@tool 
def get_extra_fundamentals(ticket: str):
    return True 


test_ticker = "ASML"
news = get_recent_news(test_ticker)
print(news)
#div = get_dividend_history(ticker)
# #print(div)