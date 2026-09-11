import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_fetcher import fetch_fundamentals, get_universe
from groq import Groq
from dotenv import load_dotenv

load_dotenv() 


JUNIOR_SCREENER_PROMPT = """You are a junior equity research analyst doing a first-pass screen.

You will receive a JSON array of stocks, pre-filtered from European exchanges
on low trailing P/E and market cap > €5B. Each record may include: ticker, name,
sector, industry, pe, forward_pe, peg, price_to_book, ev_ebitda, roe,
debt_to_equity, revenue_growth, earnings_growth, eps, net_margin, market_cap.

Task: flag 5 to 10 stocks that look potentially undervalued RELATIVE TO THEIR
INDUSTRY PEERS IN THIS TABLE — not against the market as a whole, and not
against your own knowledge of these companies. Aim for that 5-10 range: if
fewer than 5 names genuinely clear the bar, extend the list with the next
most defensible candidates, ranked lower and marked low-confidence, rather
than stopping early — the goal is a usable shortlist, not just the top 1-2
names. Only return fewer than 5 if the table genuinely doesn't have enough
distinct peer groups to support more.

For each stock you flag, in ONE compact table row — do not write prose
paragraphs or restate the raw JSON fields:
1. Ticker + a verdict of no more than 12 words.
2. The 2-3 specific numbers that matter most, compared against the closest
   peer value (e.g. "P/E 4.0 vs peer avg 9.7") — not a full field-by-field
   recap.
3. One risk or red flag in no more than 12 words — every flagged stock must
   have one, since a low P/E alone is not enough. If the low P/E is paired
   with flat or negative revenue_growth or earnings_growth, name it a
   possible value trap instead of a clean bargain.

Keep the entire response under 700 words total so all 5-10 rows fit.

Rules:
- Use only the numbers in the table. Never invent, estimate, or recall
  figures about these companies from outside knowledge.
- If a field is null/missing, say so explicitly rather than guessing or
  silently skipping it.
- A low P/E or PEG alone does not qualify a stock — corroborate with at
  least one other metric (ROE, margins, growth, or leverage).
- Only compare stocks within the same sector. If a sector has fewer than 3
  members in the table, say the comparison is low-confidence.
- Prefer including a borderline candidate (clearly marked low-confidence)
  over omitting it, so the list can reach 5-10 whenever the data supports it.
- Rank flagged stocks from most to least compelling.
- If nothing at all clears even a low-confidence bar, say so plainly instead
  of forcing a pick.

End with one sentence noting this is a first-pass screen, not investment
advice.
"""

TICKERS = get_universe()

def ask_agent(table_json: str):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": JUNIOR_SCREENER_PROMPT},
            {"role": "user", "content": f"Here is the table:\n\n{table_json}"},
        ],
        temperature=0.2,
        reasoning_effort="low",
        max_completion_tokens=1500,
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    table_json = fetch_fundamentals(TICKERS)
    result = ask_agent(table_json)
    print(result)

    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    filename = f"screener_{datetime.now():%Y%m%d_%H%M%S}.txt"
    filepath = os.path.join(results_dir, filename)
    with open(filepath, "w") as f:
        f.write(result)

    print(f"\nResults saved to {filepath}")