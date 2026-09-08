import time
import pandas as pd
import yfinance as yf
from yfinance import EquityQuery

# yfinance field name -> our column name
FIELDS = {
    "sector": "sector",
    "industry": "industry",
    "shortName": "name",
    "trailingPE": "pe",
    "forwardPE": "forward_pe",
    "pegRatio": "peg",
    "priceToBook": "price_to_book",
    "enterpriseToEbitda": "ev_ebitda",
    "returnOnEquity": "roe",
    "debtToEquity": "debt_to_equity",
    "revenueGrowth": "revenue_growth",
    "earningsGrowth": "earnings_growth",
    "trailingEps": "eps",
    "profitMargins": "net_margin",
    "marketCap": "market_cap",
}

euronext_exchanges = [
    "PAR",  # Paris
]

query = EquityQuery('and', [
    # Euronext-listed
    EquityQuery('is-in', [
        'exchange',
        *euronext_exchanges
    ]),
    # 0 < P/E < 15
    EquityQuery('btwn', [
        'peratio.lasttwelvemonths',
        0,
        15
    ]),
    # Market cap > 5 billion
    EquityQuery('gt', [
        'intradaymarketcap',
        5_000_000_000
    ])
])

def get_universe() -> list[str]:
    result = yf.screen(query, size=10, sortField='peratio.lasttwelvemonths', sortAsc=True)
    return [stock['symbol'] for stock in result['quotes']]

def fetch_fundamentals(tickers):
    rows = []
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
        except Exception as e:
            print(f"  [skip] {ticker}: fetch error ({e})")
            continue

        if not info or info.get("trailingPE") is None:
            print(f"  [skip] {ticker}: no usable PE data")
            continue

        # Skip listings where price currency and financial reporting
        # currency differ - ratios like PE/EV-EBITDA get distorted.
        if info.get("currency") != info.get("financialCurrency"):
            print(f"  [skip] {ticker}: currency mismatch "
                  f"({info.get('currency')} price vs {info.get('financialCurrency')} financials)")
            continue

        row = {"ticker": ticker}
        for src_field, out_name in FIELDS.items():
            row[out_name] = info.get(src_field)
        rows.append(row)

        time.sleep(0.1)

    return pd.DataFrame(rows)