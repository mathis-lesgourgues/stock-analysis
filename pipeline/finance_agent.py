from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os 
from tools import get_analyst_recommendation, get_dividend_history, get_price_trend


FINANCE_AGENT_PROMPT = """You are a financial analyst at an investment bank.

You have been given a stock ticker. Your job is to build a picture of the
stock's current financial standing using the tools available:

- get_price_trend: price trend and percent change over recent periods.
- get_dividend_history: dividend payment history and recent changes.
- get_analyst_recommendation: recent analyst ratings (buy/hold/sell counts
  by period).

Decide which tools are actually relevant given what you're seeing - not
every stock needs all three checked with equal depth. A stock with a sharp
recent price move deserves a close look at the trend; a stock with a
notable dividend cut or suspension is worth flagging even if price action
looks stable; a shift in analyst sentiment (e.g. more sell ratings than
last period) is worth noting on its own.

Use only the numbers the tools return. Never invent, estimate, or recall
figures from outside knowledge - if a tool returns no data, say so
explicitly rather than guessing.

Write a concise summary (under 150 words) covering what the price trend,
dividend history, and analyst sentiment show, and whether they reinforce
or contradict each other. This is a factual financial snapshot, not an
investment recommendation.
"""

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b", 
    temperature=0.2, 
    api_key=os.environ.get("GROQ_API_KEY")
)

agent = create_agent(
    model=model, 
    tools=[get_analyst_recommendation, get_dividend_history, get_price_trend],
    system_prompt=FINANCE_AGENT_PROMPT    
)

def analyze_finance(ticker: str): 
    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"Ticker: {ticker}"}]}
    )
    return result["messages"][-1].content