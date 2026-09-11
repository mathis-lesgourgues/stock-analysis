import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_fetcher import fetch_fundamentals
from junior_screener import TICKERS, ask_agent, parse_tickers
from senior_agent import analyze


def run_pipeline():
    print(f"Universe: {len(TICKERS)} tickers")

    table_json = fetch_fundamentals(TICKERS)
    screener_report = ask_agent(table_json)
    print("\n=== Junior Screener ===\n")
    print(screener_report)

    flagged = parse_tickers(screener_report)
    if not flagged:
        print("\nNo tickers parsed from screener output; skipping senior review.")
        return

    print(f"\n=== Senior Review ({len(flagged)} tickers) ===\n")
    senior_reports = {}
    for ticker in flagged:
        print(f"--- {ticker} ---")
        try:
            senior_reports[ticker] = analyze(ticker)
        except Exception as e:
            senior_reports[ticker] = f"[error] {e}"
        print(senior_reports[ticker])
        print()

    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    filename = f"pipeline_{datetime.now():%Y%m%d_%H%M%S}.txt"
    filepath = os.path.join(results_dir, filename)
    with open(filepath, "w") as f:
        f.write("=== Junior Screener ===\n\n")
        f.write(screener_report)
        f.write("\n\n=== Senior Review ===\n\n")
        for ticker, report in senior_reports.items():
            f.write(f"--- {ticker} ---\n{report}\n\n")

    print(f"Results saved to {filepath}")


if __name__ == "__main__":
    run_pipeline()
