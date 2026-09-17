from langchain.tools import tool
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from news_agent import analyze_news
from finance_agent import analyze_finance

@tool
def investigate_news(ticker: str) -> str:
    """Get a news/events analysis for this ticker - recent headlines and
    what they suggest about the company's situation."""
    return analyze_news(ticker)

@tool
def investigate_finance(ticker: str) -> str:
    """Get a financial snapshot for this ticker - price trend, dividend
    history, and analyst recommendations."""
    return analyze_finance(ticker)


MANAGER_PROMPT = """You are the lead analyst coordinating a stock review.

You have two specialist tools available:
- investigate_news: news/events analysis for a ticker
- investigate_finance: financial snapshot (price, dividends, analyst ratings)

Call whichever you need, in whatever order makes sense. You may call a
tool more than once if the first result raises something worth digging
into further - e.g. if investigate_news mentions a specific event, you can
call investigate_finance to check whether the price trend confirms it.

Once you have enough information, write a final verdict deciding whether
the situation looks structural (a real underlying problem) or conjunctural
(a temporary/overreaction situation), with your confidence level and the
key evidence behind it. This is a factual analysis, not investment advice.
"""

model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2)

manager_agent = create_agent(
    model=model,
    tools=[investigate_news, investigate_finance],
    system_prompt=MANAGER_PROMPT,
)


def analyze_company(ticker: str) -> str:
    result = manager_agent.invoke(
        {"messages": [{"role": "user", "content": f"Ticker: {ticker}"}]}
    )
    return result["messages"][-1].content