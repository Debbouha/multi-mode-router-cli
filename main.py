import sys

from pydantic import ValidationError

from models import JobOfferAnalysis, TaskExtraction
from llm_client import generate_schema_response
from prompts import build_job_offer_prompt, build_task_prompt
from display import display_result


MODE = {
    "job_offer": (JobOfferAnalysis, build_job_offer_prompt),
    "task": (TaskExtraction, build_task_prompt),
}


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in MODE:
        print(f"Usage: python main.py <{'|'.join(MODE)}> <raw_text.txt>")
        return 1
    
    mode_name = sys.argv[1]
    model_class, prompt_builder = MODE[mode_name]
    file_name = sys.argv[2]
    schema = model_class.model_json_schema()

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            raw_text = file.read()
    except FileNotFoundError:
        print(f"Error: file not found: {file_name}")
        return 1
    
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

    display_result(validated_result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())