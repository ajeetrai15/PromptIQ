"""Prompt Comparison Lab execution and dual-output comparative analysis."""

from typing import Optional, Tuple
from core.gemini_service import GeminiService
from core.schemas import ComparisonAnalysisResult


def run_comparison(
    original_prompt: str,
    improved_prompt: str,
    temperature: float = 0.7,
    service: Optional[GeminiService] = None,
) -> Tuple[str, str, ComparisonAnalysisResult]:
    """Execute both prompts against Gemini and analyze the empirical differences."""
    if not original_prompt or not original_prompt.strip():
        raise ValueError("Original prompt cannot be empty.")
    if not improved_prompt or not improved_prompt.strip():
        raise ValueError("Optimized prompt cannot be empty.")

    srv = service or GeminiService()

    # Generate both outputs
    original_output = srv.execute_raw_prompt(original_prompt.strip(), temperature=temperature)
    improved_output = srv.execute_raw_prompt(improved_prompt.strip(), temperature=temperature)

    # Perform empirical comparative analysis
    analysis = srv.compare_outputs(
        original_prompt=original_prompt.strip(),
        improved_prompt=improved_prompt.strip(),
        original_output=original_output,
        improved_output=improved_output,
    )

    return original_output, improved_output, analysis
