from tools import get_recent_news
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

load_dotenv()

NEWS_AGENT_PROMPT = """You are a financial analyst at an investment bank.

You have been given a stock ticker. Use get_recent_news to read the most
recent news articles about the company, then write a concise summary of
what's currently happening - product launches, earnings surprises,
management changes, legal/regulatory issues, restructuring, partnerships,
or anything else that could explain recent investor sentiment.

Rules:
- Only report what the articles actually say. Never invent an article,
  a fact, or a quote that wasn't in the tool's results.
- If get_recent_news returns no results, say so explicitly rather than
  guessing or making something up.
- Keep the summary under 200 words - concise, key information only.
- If the articles point to a specific reason the stock might be moving
  (up or down), call that out explicitly rather than just listing headlines.

This is a factual news summary, not investment advice.
"""

model = ChatGroq(
    model="openai/gpt-oss-120b", 
    temperature=0.2,
    api_key=os.environ.get("GROQ_API_KEY"), 
)

agent = create_agent(
    model=model, 
    tools=[get_recent_news],
    system_prompt=NEWS_AGENT_PROMPT
)

def analyze_news(ticker: str): 
    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"Ticker: {ticker}"}]}
    )
    return result["messages"][-1].content



