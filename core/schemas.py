"""Pydantic data schemas for structured Gemini outputs and validation."""

from typing import List, Optional
from pydantic import BaseModel, Field


class WeaknessItem(BaseModel):
    weakness: str = Field(description="The detected flaw or missing element in the prompt.")
    why_it_matters: str = Field(description="Clear explanation of how this flaw negatively impacts model response quality or predictability.")


class CriterionEvaluation(BaseModel):
    score: int = Field(ge=0, le=100, description="Score from 0 to 100 for this criterion.")
    rationale: str = Field(description="Detailed objective justification for why this specific score was awarded.")


class PromptAnalysisResult(BaseModel):
    overall_score: int = Field(ge=0, le=100, description="Overall weighted prompt quality score from 0 to 100.")
    scoring_basis_summary: str = Field(description="Explanation of how the overall score and criteria scores were determined.")
    
    clarity: CriterionEvaluation = Field(description="Evaluation of clarity and freedom from ambiguity.")
    context: CriterionEvaluation = Field(description="Evaluation of domain, background, and situational context.")
    specificity: CriterionEvaluation = Field(description="Evaluation of detail, precision, and boundaries.")
    task_definition: CriterionEvaluation = Field(description="Evaluation of how well the core objective is instructed.")
    output_format: CriterionEvaluation = Field(description="Evaluation of explicit structure, formatting, or styling requirements.")
    constraints: CriterionEvaluation = Field(description="Evaluation of negative constraints, limits, tone, or guardrails.")
    
    weaknesses: List[WeaknessItem] = Field(default_factory=list, description="List of detected weaknesses and their implications.")
    recommendations: List[str] = Field(default_factory=list, description="Actionable, concrete recommendations to upgrade the prompt.")


class ImprovementRow(BaseModel):
    original_element: str = Field(description="The phrasing, missing piece, or element in the original prompt.")
    improvement: str = Field(description="The refined or newly introduced element in the optimized prompt.")
    reason: str = Field(description="The prompt engineering principle and reason for this change.")


class PromptOptimizationResult(BaseModel):
    improved_prompt: str = Field(description="The fully rewritten, production-grade prompt.")
    role_defined: str = Field(description="The persona, expert identity, or role injected.")
    task_defined: str = Field(description="The precise task description provided to the model.")
    context_provided: str = Field(description="The relevant background or situational context added.")
    output_format_specified: str = Field(description="The structural or formatting constraints established.")
    constraints_applied: str = Field(description="Guardrails, tone limits, negative constraints, or boundaries added.")
    improvements_table: List[ImprovementRow] = Field(default_factory=list, description="Row-by-row breakdown of changes.")


class ObservableDifference(BaseModel):
    category: str = Field(description="Aspect observed, e.g. Specificity, Structure, Hallucination Risk, Actionability.")
    original_behavior: str = Field(description="How the original prompt response manifested.")
    improved_behavior: str = Field(description="How the improved prompt response manifested.")
    takeaway: str = Field(description="Why this difference occurred and when it matters.")


class ComparisonAnalysisResult(BaseModel):
    observable_differences: List[ObservableDifference] = Field(default_factory=list, description="Key empirical differences between the outputs.")
    comparative_summary: str = Field(description="Objective, grounded comparative analysis based solely on actual observed outputs.")
    recommendation: str = Field(description="When a user should prefer one formulation over the other.")
