from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.anthropic import Claude
from agno.tools.duckduckgo import DuckDuckGoTools

try:
    from agno.tools.tavily import TavilyTools
except ImportError:
    TavilyTools = None

try:
    from agno.tools.crawl4ai import Crawl4aiTools
except ImportError:
    Crawl4aiTools = None

try:
    from brandforge.models.content import ContentIdea
except ImportError:
    ContentIdea = dict

def create_trend_scout_agent(knowledge, db, brand_context=None) -> Agent:
    instructions = [
        "Monitor industry trends and news.",
        "Track viral content patterns across social media.",
        "Identify trending hashtags relevant to the niche.",
        "Analyze seasonal opportunities and key dates.",
        "Discover content gaps that competitors are missing.",
        "Spot emerging content formats (e.g., new video styles).",
        "Evaluate trend relevance and feasibility for the brand."
    ]

    if brand_context:
        instructions.append(f"Focus trends around this brand context: {brand_context}")

    tools = [DuckDuckGoTools(enable_search=True, enable_news=True)]
    if TavilyTools:
        tools.append(TavilyTools())
    if Crawl4aiTools:
        tools.append(Crawl4aiTools())

    return Agent(
        name="TrendScout",
        role="Trend & Opportunity Analyst",
        model=Gemini(id="gemini-3.1-pro-preview"),
        instructions=instructions,
        tools=tools,
        output_schema=list[ContentIdea],
        knowledge=knowledge,
        search_knowledge=True,
        db=db,
        add_history_to_context=True,
        num_history_runs=5,
        fallback_models=[Claude(id="claude-sonnet-4-20250514")],
        retries=3,
        exponential_backoff=True,
        markdown=True,
    )
