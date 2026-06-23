RULE_INSTRUCTIONS = """
<rules>
-Do not invent missing information.
-Return only data matching the provided JSON schema.
</rules>
"""


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