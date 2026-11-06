"""Prompt Analyzer module for evaluating prompt quality across 6 core criteria."""

from typing import Optional
from core.gemini_service import GeminiService
from core.schemas import PromptAnalysisResult


def analyze_prompt(prompt_text: str, service: Optional[GeminiService] = None) -> PromptAnalysisResult:
    """Analyze a prompt using the configured Gemini service."""
    if not prompt_text or not prompt_text.strip():
        raise ValueError("Please provide a prompt to analyze.")
    srv = service or GeminiService()
    return srv.analyze_prompt(prompt_text.strip())
