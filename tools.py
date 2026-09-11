import json
import pandas as pd
import yfinance as yf
from langchain.tools import tool

@tool
def get_recent_news(ticker: str, max_items: int = 5):
    """
    Params:
        ticker: ticker corresponding to the analyzed stock
        max_items: maximum number of news items to return
    Returns:
        list[dict]: recent news items with 'title' and 'summary', ranked most
        recent first. Empty list if no news is available for this ticker.
    """
    results = yf.Ticker(ticker).news
    items = []
    for item in results[:max_items]:
        content = item.get("content", item)
        items.append({
            "title": content.get("title"),
            "summary": content.get("summary"),
        })
    # Return a JSON string (never a bare empty list) so the tool message
    # content stays a valid non-empty string for the chat completions API.
    return json.dumps(items) if items else "No news found for this ticker."
     
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
        ticker: ticker corresponding to the analyzed stock
    Returns:
        str: JSON summary of the 1-year price trend - current price,
        percent change over 1/3/6/12 months, and 52-week high/low. This is a
        compact summary, not the raw daily OHLCV history.
    """
    hist = yf.Ticker(ticker).history(period="1y")
    if hist.empty:
        return "No price history found for this ticker."

    current_price = hist["Close"].iloc[-1]
    last_date = hist.index[-1]

    changes = {}
    for months in (1, 3, 6, 12):
        cutoff = last_date - pd.DateOffset(months=months)
        past = hist.loc[:cutoff]
        if past.empty:
            changes[f"pct_change_{months}m"] = None
            continue
        past_price = past["Close"].iloc[-1]
        changes[f"pct_change_{months}m"] = round(
            (current_price - past_price) / past_price * 100, 2
        )

    summary = {
        "current_price": round(current_price, 2),
        "52w_high": round(hist["High"].max(), 2),
        "52w_low": round(hist["Low"].min(), 2),
        **changes,
    }
    return json.dumps(summary)


@tool
def get_extra_fundamentals(ticker: str):
    """Placeholder for additional fundamentals not yet implemented."""
    return True
