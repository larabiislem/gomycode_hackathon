from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.anthropic import Claude
from agno.tools.website import WebsiteTools
from agno.tools.duckduckgo import DuckDuckGoTools

try:
    from agno.tools.crawl4ai import Crawl4aiTools
except ImportError:
    Crawl4aiTools = None

try:
    from brandforge.models.strategy import CompetitorInsight
except ImportError:
    CompetitorInsight = dict

def create_competitor_analyst_agent(knowledge, db, brand_context=None) -> Agent:
    instructions = [
        "Analyze competitor social profiles and digital presence.",
        "Track competitors' posting frequency and timing.",
        "Identify competitors' top-performing content and themes.",
        "Analyze engagement patterns and audience reactions.",
        "Find content gaps and missed opportunities in competitor strategies.",
        "Benchmark the brand's performance against key competitors."
    ]

    if brand_context:
        instructions.append(f"Consider this brand context when comparing: {brand_context}")

    tools = [WebsiteTools(), DuckDuckGoTools()]
    if Crawl4aiTools:
        tools.append(Crawl4aiTools())

    return Agent(
        name="CompetitorAnalyst",
        role="Competitive Intelligence Specialist",
        model=Gemini(id="gemini-3.1-pro-preview"),
        instructions=instructions,
        tools=tools,
        output_schema=list[CompetitorInsight],
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
