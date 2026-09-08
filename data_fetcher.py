import time
import pandas as pd
import yfinance as yf

TICKERS = [
    "MC.PA", "OR.PA", "SAN.PA", "AIR.PA", "TTE.PA",
    "BNP.PA", "SU.PA", "AI.PA", "EL.PA", "DG.PA",
    "CS.PA", "BN.PA", "RI.PA", "KER.PA", "CAP.PA",
    "SGO.PA", "STLA.PA", "ML.PA", "ENGI.PA", "VIE.PA",
    "LR.PA", "HO.PA", "GLE.PA", "ACA.PA", "DSY.PA",
    "PUB.PA", "SAF.PA", "STM.PA", "URW.PA", "WLN.PA",
]

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


import yfinance as yf
from yfinance import EquityQuery

euronext_exchanges = [
    "AMS",  # Amsterdam
    "BRU",  # Brussels
    "LIS",  # Lisbon
    "PAR",  # Paris
    "OSL",  # Oslo
    "MIL",  # Milan
    "ISE",  # Dublin
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

result = yf.screen(
    query,
    size=250,
    sortField='peratio.lasttwelvemonths',
    sortAsc=True
)

stocks = result['quotes']

tickers = [stock['symbol'] for stock in stocks]

print(f"{len(tickers)} stocks found")

stocks = result['quotes']

for stock in stocks:
    print(
        stock.get('symbol'),
        stock.get('shortName'),
        stock.get('exchange'),
        stock.get('region'),
        stock.get('trailingPE')
    )

"""
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

        row = {"ticker": ticker}
        for src_field, out_name in FIELDS.items():
            row[out_name] = info.get(src_field)
        rows.append(row)

        time.sleep(0.15)  # in order not to crash the endpoint 

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = fetch_fundamentals(TICKERS)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    print(df)
"""