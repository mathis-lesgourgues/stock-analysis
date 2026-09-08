import os
import json

from data_fetcher import fetch_fundamentals, get_universe
from groq import Groq
from dotenv import load_dotenv

load_dotenv() 

## to split in different prompts : financial analyst prompt, debt analyst prompt, 
## news analyst prompt 

SYSTEM_PROMPT = """You are an equity analyst reviewing a table of stocks.
Each stock has a sector label and valuation/growth metrics.

Identify which stocks look potentially undervalued.

For each stock you flag, explain briefly why, referencing the actual
numbers and comparing to sector peers in this table.

If nothing looks clearly undervalued, say so.
"""

TICKERS = get_universe()

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

if __name__ == "__main__":
    df = fetch_fundamentals(TICKERS)   
    records = df.to_dict(orient="records")
    print(ask_agent(records))
    pass