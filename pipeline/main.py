import sys
from datetime import datetime

from manager_agent import analyze_company
from utils import get_ticker_from_company_name

def main():
    company_name = input("Company name : ").strip()
    if not company_name:
        print("No company written")
        sys.exit(1)

    ticker = get_ticker_from_company_name(company_name)
    if not ticker:
        print(f"No ticker found for '{company_name}'.")
        sys.exit(1)

    print(f"Ticker trouvé : {ticker}\n")
 
    report = analyze_company(ticker)
    print(report)

if __name__ == "__main__":
    main()
