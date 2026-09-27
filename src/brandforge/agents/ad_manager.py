from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.anthropic import Claude

try:
    from brandforge.config.settings import settings
    from brandforge.tools.meta_ads import MetaAdsToolkit
except ImportError:
    settings = None
    class MetaAdsToolkit:
        def __init__(self, **kwargs):
            pass

try:
    from brandforge.models.advertising import AdCampaign
except ImportError:
    AdCampaign = dict

def create_ad_manager_agent(knowledge, db, brand_context=None) -> Agent:
    instructions = [
        "Create Meta Ads campaigns perfectly aligned with strategic objectives.",
        "Define precise targeting based on established audience personas.",
        "Set smart budget allocations across ad sets.",
        "Create compelling and high-converting ad copy.",
        "Continuously monitor active campaign performance.",
        "Optimize bids and targeting to lower CPA.",
        "Structure and execute A/B tests on creatives and copy.",
        "Manage the complete end-to-end campaign lifecycle."
    ]

    if brand_context:
        instructions.append(f"Align ad messaging with this brand context: {brand_context}")

    tools = []
    try:
        if settings and hasattr(settings, 'META_ACCESS_TOKEN'):
            tools.append(MetaAdsToolkit(
                access_token=settings.META_ACCESS_TOKEN,
                ad_account_id=settings.META_AD_ACCOUNT_ID
            ))
    except Exception:
        pass

    return Agent(
        name="AdManager",
        role="Paid Media Campaign Manager",
        model=Gemini(id="gemini-3.1-pro-preview"),
        instructions=instructions,
        tools=tools,
        output_schema=AdCampaign,
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
