from typing import Literal

from pydantic import BaseModel, Field


class Skill(BaseModel):
    name: str = Field(description="Skill name.")
    category: Literal[
        "language",
        "framework",
        "tool",
        "cloud",
        "soft_skill",
        "other",
    ] = Field(description="Skill category.")


class JobOfferAnalysis(BaseModel):
    title: str = Field(description="Job title.")
    company: str | None = Field(default=None, description="Company name.")
    location: str | None = Field(default=None, description="Job location.")
    contract_type: Literal[
        "full_time",
        "part_time",
        "freelance",
        "internship",
        "apprenticeship",
        "unknown",
    ] = Field(default="unknown", description="Contract type.")
    seniority: Literal["junior", "mid", "senior", "lead", "unknown"] = Field(
        default="unknown",
        description="Job seniority.",
    )
    required_skills: list[Skill] = Field(
        description="Skills required for the position."
    )
    nice_to_have_skills: list[Skill] = Field(
        description="Additional skills that are beneficial but not required."
    )
    summary: str = Field(description="Short job summary.")


class Task(BaseModel):
    title: str = Field(description="Task title.")
    priority: Literal["low", "medium", "high", "unknown"] = Field(
        default="unknown",
        description="Priority level.",
    )
    due_date: str | None = Field(default=None, description="Due date ISO 8601 format.")
    assignee: str | None = Field(default=None, description="Assignee name.")
    is_blocking: bool = Field(description="Whether the task blocks other tasks.")


class TaskExtraction(BaseModel):
    source_message: str = Field(description="Original message content.")
    tasks: list[Task] = Field(description="Tasks list.")