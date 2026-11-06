"""Prompt Optimizer module for rewriting prompts to meet professional standards."""

from typing import Optional
from core.gemini_service import GeminiService
from core.schemas import PromptOptimizationResult


def optimize_prompt(prompt_text: str, service: Optional[GeminiService] = None) -> PromptOptimizationResult:
    """Optimize a prompt and generate structured diff table."""
    if not prompt_text or not prompt_text.strip():
        raise ValueError("Please provide a prompt to optimize.")
    srv = service or GeminiService()
    return srv.optimize_prompt(prompt_text.strip())
