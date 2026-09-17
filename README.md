# Agentic Stock Analysis

A small multi-agent system that takes a company name, resolves it to a stock
ticker, and produces a short research report combining recent news, a
financial snapshot, and industry context - built with LangChain and Groq.

## How it works

1. You enter a company name in the terminal.
2. `utils.py` resolves that name to a Yahoo Finance ticker.
3. `manager_agent.py` coordinates the analysis. It has three specialist
   agents available as tools and decides which ones to call, in what order,
   and whether to call one again if the first results raise a question
   worth digging into further.
4. Each specialist agent runs its own reasoning loop with its own tools:
   - `news_agent.py` - reads recent news headlines and summarizes what's
     currently happening with the company.
   - `finance_agent.py` - looks at price trend, dividend history, and
     analyst recommendations.
   - `industry_agent.py` - looks at the company's industry context.
5. The manager combines what it learns into a final verdict: whether the
   situation looks structural (a real underlying issue) or conjunctural
   (a temporary move), with a confidence level and the evidence behind it.

This is a research/diagnostic tool, not investment advice - it's meant to
help narrow down what's worth looking into further, not to make a buy/sell
call on its own.

## Project structure

```
pipeline/
  main.py              entry point - takes a company name, runs the pipeline
  manager_agent.py      coordinates the specialist agents
  news_agent.py          news/events specialist
  finance_agent.py        financial snapshot specialist
  tools.py                shared tool functions (news, price trend,
                           dividends, analyst recommendations, insider
                           purchases, industry data)
  utils.py                 

```

## Design notes

- **Tools are deliberately deterministic** Every function in `tools.py` is a
  plain, deterministic lookup - no reasoning happens inside them. The
  judgment (which tool to call, how to interpret the result, when to stop
  investigating) is entirely the LLM's job. This split is what makes the
  system agentic rather than a fixed pipeline with an LLM step glued in.
- **The manager doesn't repeat work the specialists already did.** It
  receives each specialist's report and reasons over it, rather than
  recomputing financial ratios or re-reading news itself.
- **Every response notes this isn't investment advice.** The agents
  produce a diagnosis, not a recommendation - the decision to act stays
  with the user.

## Known limitations

- Ticker resolution via `yfinance`'s search isn't always exact - for
  companies with multiple listings or common names, it may pick a
  cross-listed or unrelated match. Worth a quick sanity check on the
  resolved ticker before trusting the report.
- `yfinance` is an unofficial data source; some fields are occasionally
  missing or inconsistent for smaller or less-covered companies.
- Token usage can add up quickly for a single ticker, since the manager
  and each specialist agent all make their own LLM calls. Worth keeping
  an eye on if you're on a free-tier API plan.

## Possible next steps

- RAG over full earnings call transcripts or annual reports, for a deeper
  read than headlines alone can give.
- Letting the manager send a specialist back for a second, more targeted
  look instead of always taking the first report at face value.
- A small scheduled version that watches a fixed list of holdings and
  flags only meaningful changes, rather than requiring a manual lookup
  each time.