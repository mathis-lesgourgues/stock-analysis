from tools import get_recent_news
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

load_dotenv()

NEWS_AGENT_PROMPT = """
You are a financial analyst at an investment bank and your job is to read the recent newspapers articles about a company and \\ 
and do a quick summary about it. 

Rules : 
    - Don't create articles, don't use articles you did not read on the news.
    - The summary must be 200 words maximum, it needs to be concise with key information
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



