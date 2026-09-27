from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools

try:
    from brandforge.tools.analytics_tools import AnalyticsToolkit
except ImportError:
    class AnalyticsToolkit:
        pass

try:
    from brandforge.models.analytics import PerformanceReport
except ImportError:
    PerformanceReport = dict

def create_optimizer_agent(knowledge, db, brand_context=None) -> Agent:
    instructions = [
        "Analyze historical performance data deeply.",
        "Identify hidden patterns and commonalities in high-performing content.",
        "Recommend specific strategic pivots based on data.",
        "Suggest data-backed content mix and format adjustments.",
        "Optimize future posting schedules for maximum reach.",
        "Recommend budget reallocation across campaigns based on ROI.",
        "Predict future content performance using historical baselines.",
        "Continuously learn from new data and adapt strategies accordingly."
    ]

    if brand_context:
        instructions.append(f"Consider long-term goals from this brand context: {brand_context}")

    tools = [ReasoningTools(add_instructions=True)]
    try:
        tools.append(AnalyticsToolkit())
    except Exception:
        pass

    return Agent(
        name="Optimizer",
        role="AI Strategy Optimizer",
        model=Gemini(id="gemini-3.1-pro-preview"),
        instructions=instructions,
        tools=tools,
        output_schema=PerformanceReport, # Output should include strategy_adjustments
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
