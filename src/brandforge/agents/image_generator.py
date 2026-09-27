from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.anthropic import Claude
from agno.tools.openai import OpenAITools

try:
    from agno.tools.fal import FalTools
except ImportError:
    FalTools = None

def create_image_generator_agent(knowledge, db, brand_context=None) -> Agent:
    instructions = [
        "Generate stunning social media visuals based directly on creative briefs.",
        "Create strictly on-brand imagery reflecting correct styles and moods.",
        "Produce platform-optimized graphics considering correct dimensions.",
        "Generate thumbnail variations to test performance.",
        "Create engaging story and reel cover images."
    ]

    if brand_context:
        instructions.append(f"Incorporate this brand context into visual aesthetics: {brand_context}")

    tools = [OpenAITools(image_model='dall-e-3')] # Using dall-e-3 as standard for GPT image gen
    if FalTools:
        tools.append(FalTools())

    return Agent(
        name="ImageGenerator",
        role="AI Visual Content Creator",
        model=Gemini(id="gemini-3.1-flash-preview"),
        instructions=instructions,
        tools=tools,
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
