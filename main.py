import sys

from pydantic import ValidationError

from display import display_result
from router import route_input
from pipeline import run_pipeline


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
    
    route = route_decision.route
    
    try:
        validated_result = run_pipeline(raw_text, route)
    except ValueError as err:
        print(err)
        return 1
    except RuntimeError as err:
        print(f"Gemini error: {err}")
        return 1
    except ValidationError:
        print("Error: response does not match schema")
        return 1
    
    display_result(route_decision)
    display_result(validated_result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())