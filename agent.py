import os
import json

from data_fetcher import fetch_fundamentals, TICKERS
from groq import Groq
from dotenv import load_dotenv

load_dotenv() 

SYSTEM_PROMPT = """You are an equity analyst reviewing a table of stocks.
Each stock has a sector label and valuation/growth metrics.

Identify which stocks look potentially undervalued.

For each stock you flag, explain briefly why, referencing the actual
numbers and comparing to sector peers in this table.

If nothing looks clearly undervalued, say so.

## Capabilities: 

- `get_price_trend`: get the trend of a specific stock over a passed period of time 

- `get_recent_news`: get some recent news about a specific stock

- `get_extra_fundamentals`: get some extra financial fundamentals abotu a specific stock 
"""

def ask_agent(records: list[dict]):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    table_text = json.dumps(records, indent=2, default=str)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Here is the table:\n\n{table_text}"},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


build_agent()

run_agent()


if __name__ == "__main__":
    df = fetch_fundamentals(TICKERS)   
    records = df.to_dict(orient="records")
    print(ask_agent(records))
    pass