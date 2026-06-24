import sys

from pydantic import ValidationError

from models import JobOfferAnalysis, TaskExtraction, Recipe
from llm_client import generate_schema_response
from prompts import build_job_offer_prompt, build_task_prompt, build_recipe_prompt
from display import display_result
from router import route_input


MODE = {
    "job_offer_analysis": (JobOfferAnalysis, build_job_offer_prompt),
    "task_extraction": (TaskExtraction, build_task_prompt),
    "recipe_generation": (Recipe, build_recipe_prompt),
}


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: python main.py <raw_text.txt>")
        return 1

    file_name = sys.argv[1]

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            raw_text = file.read()
    except FileNotFoundError:
        print(f"Error: file not found: {file_name}")
        return 1

    try:
        route_decision = route_input(raw_text)

    except RuntimeError as err:
        print(f"Gemini error: {err}")
        return 1

    except ValidationError as err:
        print("Router validation error")
        print(err)
        return 1

    if (
        route_decision.route == "unknown" or
        route_decision.confidence == "low" or
        route_decision.needs_clarification
    ):
        display_result(route_decision)
        return 0
    
    mode_name = route_decision.route
    if mode_name not in MODE:
        print("unsupported route")
        display_result(route_decision)
        return 1
    model_class, prompt_builder = MODE[mode_name]
    schema = model_class.model_json_schema()
    prompt = prompt_builder(raw_text)
    
    try:
        response = generate_schema_response(prompt, schema)
    except RuntimeError as err:
        print(f"Error: {err}")
        return 1
    
    try:
        validated_result = model_class.model_validate_json(response)
    except ValidationError:
        print("Error: response does not match schema")
        return 1
    
    display_result(route_decision)
    display_result(validated_result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())