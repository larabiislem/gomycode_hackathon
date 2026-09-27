from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.anthropic import Claude
from agno.tools.duckdb import DuckDbTools
from agno.tools.pandas import PandasTools
from agno.tools.visualization import VisualizationTools

try:
    from brandforge.tools.analytics_tools import AnalyticsToolkit
except ImportError:
    class AnalyticsToolkit:
        pass

try:
    from brandforge.models.analytics import PerformanceReport
except ImportError:
    PerformanceReport = dict

def create_analytics_agent(knowledge, db, brand_context=None) -> Agent:
    instructions = [
        "Track essential KPIs across all active social platforms.",
        "Accurately compute engagement rates, CTRs, and ROI.",
        "Identify the top and bottom performing content pieces.",
        "Generate comprehensive visual reports with insightful charts.",
        "Detect underlying performance trends over time.",
        "Benchmark metrics against established industry standards.",
        "Provide clear, actionable, data-driven insights."
    ]

    if brand_context:
        instructions.append(f"Correlate data findings with this brand context: {brand_context}")

    tools = [
        DuckDbTools(),
        PandasTools(),
        VisualizationTools(output_dir='data/generated/reports')
    ]
    try:
        tools.append(AnalyticsToolkit())
    except Exception:
        pass

    return Agent(
        name="AnalyticsAgent",
        role="Performance Analytics Specialist",
        model=Gemini(id="gemini-3.1-pro-preview"),
        instructions=instructions,
        tools=tools,
        output_schema=PerformanceReport,
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
