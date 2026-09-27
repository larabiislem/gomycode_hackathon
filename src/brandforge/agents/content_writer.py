from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.anthropic import Claude

try:
    from brandforge.tools.content_tools import ContentToolkit
except ImportError:
    class ContentToolkit:
        pass

try:
    from brandforge.models.content import SocialPost
except ImportError:
    SocialPost = dict

def create_content_writer_agent(knowledge, db, brand_context=None) -> Agent:
    instructions = [
        "Write platform-optimized captions tailored for each network.",
        "Craft scroll-stopping hooks to capture immediate attention.",
        "Write clear and compelling Calls-to-Action (CTAs).",
        "Select highly relevant hashtags, blending popular and niche tags.",
        "Maintain strict brand voice consistency across all copy.",
        "Optimize text layout for readability and engagement.",
        "Create A/B variations for high-priority posts.",
        "Adapt tone dynamically per platform (e.g., casual on IG, professional on LinkedIn)."
    ]

    if brand_context:
        instructions.append(f"Apply this brand context: {brand_context}")

    tools = []
    try:
        tools.append(ContentToolkit())
    except Exception:
        pass

    return Agent(
        name="ContentWriter",
        role="Social Media Copywriter",
        model=Gemini(id="gemini-3.1-pro-preview"),
        instructions=instructions,
        tools=tools,
        output_schema=SocialPost,
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
