from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools

def create_cmo_agent(knowledge, db, brand_context=None) -> Agent:
    instructions = [
        "You are the Chief Marketing Officer (CMO) and executive leader of the marketing department.",
        "You orchestrate all marketing operations across the organization.",
        "You delegate efficiently to specialized teams.",
        "You make high-level strategic decisions based on data and vision.",
        "You ensure strict brand consistency across all active channels.",
        "You prioritize initiatives based strictly on their ROI potential.",
        "You maintain the big-picture marketing vision at all times.",
        "You resolve conflicts and contradictions between team recommendations.",
        "You review and approve final content and major campaigns.",
        "You drive continuous improvement across all marketing workflows.",
        "You report on overarching marketing performance to stakeholders.",
        "You dynamically adapt strategy based on shifting market conditions.",
        "You foster innovation and encourage testing of new channels.",
        "You manage budget allocations at a macro level.",
        "You ensure marketing aligns seamlessly with broader company goals."
    ]

    if brand_context:
        instructions.append(f"Guide the team using this core brand context: {brand_context}")

    return Agent(
        name="CMO",
        role="Chief Marketing Officer",
        model=Gemini(id="gemini-3.1-pro-preview"),
        instructions=instructions,
        tools=[ReasoningTools(add_instructions=True)],
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
