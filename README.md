# Multi-Mode Router CLI

Python CLI that routes a raw user message to the right structured Gemini pipeline.

The program first asks Gemini to classify the input into one of several modes, validates the routing decision with Pydantic, then calls the matching structured output pipeline.

## Flow

```text
raw text
→ Gemini router
→ RouteDecision validation
→ pipeline registry lookup
→ model + prompt selection
→ Gemini structured output
→ Pydantic validation
→ display result
```

## Supported routes

```text
task_extraction
job_offer_analysis
recipe_generation
unknown
```

If the router returns `unknown`, `low` confidence, or requires clarification, the program stops before calling the business pipeline.

## Project structure

```text
multi-mode-router-cli/
  main.py
  config.py
  models.py
  llm_client.py
  prompts.py
  router.py
  pipeline.py
  registry.py
  display.py
  samples/
```

## Run

```bash
python main.py samples/task_message.txt
python main.py samples/job_offer.txt
python main.py samples/recipe_request.txt
python main.py samples/ambiguous.txt
```

## Models

The project uses Pydantic models as contracts:

```text
RouteDecision
TaskExtraction
JobOfferAnalysis
Recipe
```

Each Gemini response is validated before being used by the program.