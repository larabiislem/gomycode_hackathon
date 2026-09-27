from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.anthropic import Claude
from agno.tools.file_generation import FileGenerationTools

try:
    from brandforge.models.creative import CreativeBrief
except ImportError:
    CreativeBrief = dict

def create_creative_director_agent(knowledge, db, brand_context=None) -> Agent:
    instructions = [
        "Create detailed visual briefs for designers and creators.",
        "Define comprehensive mood boards conveying desired aesthetics.",
        "Specify precise color palettes strictly aligned with brand guidelines.",
        "Outline clear composition and layout guidelines.",
        "Select and describe reference images to inspire design.",
        "Specify exact format and dimension requirements per platform.",
        "Communicate the core brand visual identity effectively."
    ]

    if brand_context:
        instructions.append(f"Align visuals with this brand context: {brand_context}")

    return Agent(
        name="CreativeDirector",
        role="Visual Strategy & Briefs",
        model=Gemini(id="gemini-3.1-pro-preview"),
        instructions=instructions,
        tools=[FileGenerationTools(output_directory='data/generated/briefs')],
        output_schema=CreativeBrief,
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
