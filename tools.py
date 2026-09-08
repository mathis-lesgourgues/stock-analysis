import time
import pandas as pd
import yfinance as yf

ticker = "TTE"


def get_recent_news(ticker: str): 
    search = yf.Search(ticker)
    print(search.news)

def get_price_trend(ticker: str): 
    return True 

def get_extra_fundamentals(ticket: str):
    return True 


if __name__ == "__main__":
    get_recent_news(ticker)