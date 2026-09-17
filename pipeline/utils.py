import yfinance as yf 

def get_ticker_from_company_name(company_name: str) -> str | None:
    """Search Yahoo Finance for a company name and return the best-match ticker."""
    results = yf.Search(company_name).quotes
    if not results:
        return None
    return results[0].get("symbol")