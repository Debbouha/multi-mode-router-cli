from pydantic import BaseModel

from registry import PIPELINE_REGISTRY, PipelineRoute
from llm_client import generate_schema_response


def run_pipeline(raw_text: str, route: PipelineRoute) -> BaseModel:

    if route not in PIPELINE_REGISTRY:
        raise ValueError(f"Unsupported route: {route}")
    
    model_class, prompt_builder = PIPELINE_REGISTRY[route]
    schema = model_class.model_json_schema()
    prompt = prompt_builder(raw_text)
    response = generate_schema_response(prompt, schema)
    validated_result = model_class.model_validate_json(response)

    return validated_result