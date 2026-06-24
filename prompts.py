RULE_INSTRUCTIONS = """
<rules>
-Do not invent missing information.
-Return only data matching the provided JSON schema.
</rules>
"""


def build_router_prompt(raw_text: str) -> str:
    prompt = f"""
<task>
Classify the user request into the most appropriate processing route.
</task>

<allowed_routes>
- task_extraction
- job_offer_analysis
- recipe_generation
- unknown
</allowed_routes>

<text>
{raw_text}
</text>

<rules>
- You are a routing classifier, not a business extractor.
- Do not extract tasks.
- Do not analyze the job offer.
- Do not generate a recipe.
- Choose only one route from the allowed routes.
- If the request is ambiguous, choose unknown and set confidence to low.
- If more information is required before processing, set needs_clarification to true.
- If needs_clarification is true, provide a short clarification question.
- If needs_clarification is false, clarification_question must be null.
- Keep the reason short.
</rules>
"""

    return prompt


def build_recipe_prompt(raw_text: str) -> str:
    prompt = f"""
<task>
Extract the recipe from the text below.
</task>

<text>
{raw_text}
</text>

{RULE_INSTRUCTIONS}
"""

    return prompt


def build_job_offer_prompt(raw_text: str) -> str:
    prompt = f"""
<task>
Extract the job offer information from the text below.
</task>

<text>
{raw_text}
</text>

{RULE_INSTRUCTIONS}
"""

    return prompt


def build_task_prompt(raw_text: str) -> str:
    prompt = f"""
<task>
Extract all requested tasks from the text below.
</task>

<text>
{raw_text}
</text>

{RULE_INSTRUCTIONS}
"""

    return prompt