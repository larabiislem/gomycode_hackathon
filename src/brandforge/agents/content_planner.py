from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.anthropic import Claude
from agno.tools.file import FileTools

try:
    from brandforge.models.content import ContentCalendar
except ImportError:
    ContentCalendar = dict

def create_content_planner_agent(knowledge, db, brand_context=None) -> Agent:
    instructions = [
        "Create comprehensive weekly and monthly content calendars aligned with strategy.",
        "Balance content pillars according to their strategic ratios.",
        "Schedule posts for optimal times based on audience activity.",
        "Plan platform-specific content variations.",
        "Account for relevant holidays, industry events, and seasonal trends.",
        "Ensure content variety to maintain audience interest.",
        "Maintain visual and messaging consistency across the timeline."
    ]

    if brand_context:
        instructions.append(f"Adhere to this brand context: {brand_context}")

    return Agent(
        name="ContentPlanner",
        role="Content Calendar Strategist",
        model=Gemini(id="gemini-3.1-pro-preview"),
        instructions=instructions,
        tools=[FileTools()],
        output_schema=ContentCalendar,
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
