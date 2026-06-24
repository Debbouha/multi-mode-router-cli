from typing import Callable, Literal
from pydantic import BaseModel

from models import JobOfferAnalysis, TaskExtraction, Recipe
from prompts import build_job_offer_prompt, build_task_prompt, build_recipe_prompt

PipelineRoute = Literal[
    "job_offer_analysis",
    "task_extraction",
    "recipe_generation",
]

PipelineConfig = tuple[type[BaseModel], Callable[[str], str]]

PIPELINE_REGISTRY: dict[PipelineRoute, PipelineConfig] = {
    "job_offer_analysis": (JobOfferAnalysis, build_job_offer_prompt),
    "task_extraction": (TaskExtraction, build_task_prompt),
    "recipe_generation": (Recipe, build_recipe_prompt),
}