from models import RouteDecision
from prompts import build_router_prompt
from llm_client import generate_schema_response


def route_input(raw_text: str) -> RouteDecision:
    schema = RouteDecision.model_json_schema()
    prompt = build_router_prompt(raw_text)
    response = generate_schema_response(prompt, schema)
    route_decision = RouteDecision.model_validate_json(response)

    return route_decision