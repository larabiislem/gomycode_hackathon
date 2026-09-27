from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.anthropic import Claude
from agno.tools.file import FileTools

try:
    from brandforge.models.strategy import MarketingStrategy
except ImportError:
    MarketingStrategy = dict

def create_brand_strategist_agent(knowledge, db, brand_context=None) -> Agent:
    instructions = [
        "Analyze the core brand DNA and value proposition.",
        "Define clear and compelling brand positioning in the market.",
        "Identify and profile target audience segments.",
        "Create engaging content pillars that resonate with the audience.",
        "Set measurable and achievable marketing objectives.",
        "Define the brand's tone of voice and communication style.",
        "Map the competitor landscape and identify white spaces.",
        "Recommend optimal content mix ratios across pillars.",
        "Set recommended posting frequency per platform.",
        "Align all strategic recommendations with overarching business goals.",
        "Incorporate brand context and historical data where relevant."
    ]

    if brand_context:
        instructions.append(f"Consider the following brand context: {brand_context}")

    return Agent(
        name="BrandStrategist",
        role="Brand Strategy Specialist",
        model=Gemini(id="gemini-3.1-pro-preview"),
        instructions=instructions,
        tools=[FileTools()],
        output_schema=MarketingStrategy,
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
