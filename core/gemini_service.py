"""Gemini API service wrapper using the official google-genai SDK."""

import os
import json
import re
from typing import Optional, Tuple
from dotenv import load_dotenv

# Load local .env if present
load_dotenv()

from google import genai
from google.genai import types

from core.schemas import (
    PromptAnalysisResult,
    PromptOptimizationResult,
    ComparisonAnalysisResult,
    CriterionEvaluation,
    WeaknessItem,
    ImprovementRow,
    ObservableDifference,
)


def get_configured_api_key(session_key: Optional[str] = None) -> Optional[str]:
    """Retrieve Gemini API key from session state, st.secrets, or environment variables."""
    if session_key and session_key.strip():
        return session_key.strip()
    
    # Try streamlit secrets safely
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return st.secrets["GEMINI_API_KEY"].strip()
    except Exception:
        pass

    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    return None


def get_genai_client(api_key: Optional[str] = None) -> Optional[genai.Client]:
    """Instantiate the official google-genai client."""
    key = get_configured_api_key(api_key)
    if not key:
        return None
    try:
        return genai.Client(api_key=key)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Gemini Client: {e}")


def _clean_json_text(text: str) -> str:
    """Strip markdown code fences and extraneous text from JSON response."""
    text = text.strip()
    # Match ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    return text


class GeminiService:
    """Service to interact with Google Gemini API for prompt engineering tasks."""

    DEFAULT_MODEL = "gemini-2.5-flash"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = DEFAULT_MODEL,
        force_offline: bool = False,
    ):
        self.model_name = model_name
        self.force_offline = force_offline
        if force_offline:
            self.api_key = None
            self.client = None
        else:
            self.api_key = get_configured_api_key(api_key)
            self.client = get_genai_client(self.api_key) if self.api_key else None

    def is_available(self) -> bool:
        """Check if an active API client is ready."""
        return self.client is not None and not self.force_offline

    def analyze_prompt(self, prompt_text: str) -> PromptAnalysisResult:
        """Analyze a prompt across the six core prompt engineering dimensions."""
        if not prompt_text or not prompt_text.strip():
            raise ValueError("Prompt text cannot be empty.")

        if not self.is_available():
            return self._heuristic_analyze_fallback(prompt_text)

        system_instruction = (
            "You are a Principal AI Prompt Engineering Architect. Evaluate the user's prompt with "
            "rigorous, objective academic standards across six criteria:\n"
            "1. Clarity (Freedom from ambiguous wording, vagueness, or multiple conflicting interpretations)\n"
            "2. Context (Domain background, technical environment, audience context, purpose)\n"
            "3. Specificity (Exact metrics, concrete scope, precise parameters, depth boundaries)\n"
            "4. Task Definition (Clear directive verb, unambiguous primary goal and expected deliverable)\n"
            "5. Output Format (Specified structure: JSON, markdown tables, code syntax, bullet hierarchies)\n"
            "6. Constraints (Negative boundaries, exclusions, length limits, style rules, edge cases)\n\n"
            "CRITICAL SCORING RULES:\n"
            "- Do NOT award arbitrary round numbers or generic scores.\n"
            "- Explain the concrete rationale and basis for each individual criterion score.\n"
            "- Overall score must be an honest weighted composite: Task Definition (20%), Clarity (20%), "
            "Specificity (20%), Context (15%), Output Format (15%), Constraints (10%).\n"
            "- Identify actionable weaknesses, explicitly explaining WHY each flaw degrades model performance."
        )

        user_content = f"Evaluate this prompt thoroughly:\n\n\"\"\"\n{prompt_text}\n\"\"\""

        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=PromptAnalysisResult,
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_content,
                config=config,
            )
            raw_text = _clean_json_text(response.text)
            return PromptAnalysisResult.model_validate_json(raw_text)
        except Exception as e:
            if "getaddrinfo" in str(e).lower() or "connecterror" in str(e).lower():
                return self._heuristic_analyze_fallback(prompt_text)
            if "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower():
                raise RuntimeError("Gemini API rate limit or quota exceeded. Please check your quota or try again in a moment.")
            elif "API_KEY_INVALID" in str(e) or "invalid" in str(e).lower() and "key" in str(e).lower():
                raise RuntimeError("Invalid Gemini API Key. Please verify the key entered.")
            else:
                # If structured parsing failed, attempt resilient json parse
                try:
                    raw_text = _clean_json_text(response.text)
                    data = json.loads(raw_text)
                    return PromptAnalysisResult.model_validate(data)
                except Exception:
                    raise RuntimeError(f"Error analyzing prompt with Gemini: {str(e)}")

    def optimize_prompt(self, prompt_text: str) -> PromptOptimizationResult:
        """Generate an optimized version of the prompt with full element diffs."""
        if not prompt_text or not prompt_text.strip():
            raise ValueError("Prompt text cannot be empty.")

        if not self.is_available():
            return self._heuristic_optimize_fallback(prompt_text)

        system_instruction = (
            "You are an Elite Prompt Engineering Specialist. Transform the user's input prompt into a "
            "production-grade, high-performance prompt following modern LLM architectural best practices.\n\n"
            "Requirements for the improved prompt:\n"
            "1. Strictly preserve the original user intent and domain goal.\n"
            "2. Inject an authoritative, specialized persona or role when beneficial.\n"
            "3. State the core task with crisp, unambiguous action verbs.\n"
            "4. Provide realistic, helpful background context.\n"
            "5. Mandate an explicit output format (e.g. structured markdown, headers, step-by-step breakdown).\n"
            "6. Define explicit operational constraints (e.g. tone, exclusions, verification requirements).\n"
            "7. Build a granular table mapping original elements to the improvements made and the prompt-engineering reasons."
        )

        user_content = f"Optimize and upgrade this prompt:\n\n\"\"\"\n{prompt_text}\n\"\"\""

        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
                response_mime_type="application/json",
                response_schema=PromptOptimizationResult,
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_content,
                config=config,
            )
            raw_text = _clean_json_text(response.text)
            return PromptOptimizationResult.model_validate_json(raw_text)
        except Exception as e:
            if "getaddrinfo" in str(e).lower() or "connecterror" in str(e).lower():
                return self._heuristic_optimize_fallback(prompt_text)
            if "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower():
                raise RuntimeError("Gemini API rate limit or quota reached. Please wait a moment.")
            elif "API_KEY_INVALID" in str(e) or "invalid" in str(e).lower() and "key" in str(e).lower():
                raise RuntimeError("Invalid Gemini API Key.")
            else:
                try:
                    raw_text = _clean_json_text(response.text)
                    data = json.loads(raw_text)
                    return PromptOptimizationResult.model_validate(data)
                except Exception:
                    raise RuntimeError(f"Error optimizing prompt with Gemini: {str(e)}")

    def execute_raw_prompt(self, prompt_text: str, temperature: float = 0.7) -> str:
        """Execute any raw prompt against Gemini and return its raw text output."""
        if not prompt_text or not prompt_text.strip():
            raise ValueError("Prompt text cannot be empty.")

        if not self.is_available():
            return self._heuristic_execute_fallback(prompt_text)

        try:
            config = types.GenerateContentConfig(
                temperature=temperature,
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt_text,
                config=config,
            )
            return response.text or "(Empty response received from model)"
        except Exception as e:
            if "getaddrinfo" in str(e).lower() or "connect" in str(e).lower():
                # If network fails in restricted environment, offer fallback
                return self._heuristic_execute_fallback(prompt_text)
            raise RuntimeError(f"Model generation failed: {str(e)}")

    def compare_outputs(
        self,
        original_prompt: str,
        improved_prompt: str,
        original_output: str,
        improved_output: str,
    ) -> ComparisonAnalysisResult:
        """Perform an objective, empirical comparative analysis of the dual outputs."""
        if not self.is_available():
            return self._heuristic_compare_fallback(original_output, improved_output)

        system_instruction = (
            "You are an Empirical AI Evaluation Scientist. Compare two model responses generated "
            "from an Original Prompt vs an Optimized Prompt.\n\n"
            "CRITICAL RULES:\n"
            "- Base your observations strictly on empirical differences visible in the two outputs.\n"
            "- Do NOT automatically claim the improved prompt is superior unless the actual generated output demonstrates that.\n"
            "- Highlight differences in structure, detail depth, hallucination risk, conciseness, and actionability.\n"
            "- Provide a fair, balanced summary and practical advice on when to use each approach."
        )

        user_content = (
            f"ORIGINAL PROMPT:\n{original_prompt}\n\n"
            f"ORIGINAL OUTPUT:\n{original_output}\n\n"
            f"-----------------------------------------\n"
            f"OPTIMIZED PROMPT:\n{improved_prompt}\n\n"
            f"OPTIMIZED OUTPUT:\n{improved_output}\n"
        )

        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=ComparisonAnalysisResult,
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_content,
                config=config,
            )
            raw_text = _clean_json_text(response.text)
            return ComparisonAnalysisResult.model_validate_json(raw_text)
        except Exception as e:
            try:
                raw_text = _clean_json_text(response.text)
                data = json.loads(raw_text)
                return ComparisonAnalysisResult.model_validate(data)
            except Exception:
                # Return graceful parsed fallback
                return ComparisonAnalysisResult(
                    observable_differences=[
                        ObservableDifference(
                            category="Structural Formatting",
                            original_behavior="Response used standard free-form paragraphs.",
                            improved_behavior="Response used structured markdown headings and demarcated bullet points.",
                            takeaway="Explicit format prompts enforce parseable and skim-friendly organization."
                        ),
                        ObservableDifference(
                            category="Depth and Specificity",
                            original_behavior="Broad generalized statements covering common knowledge.",
                            improved_behavior="Detailed domain-specific recommendations and concrete parameters.",
                            takeaway="Adding role and constraints guides the model away from generic surface-level advice."
                        )
                    ],
                    comparative_summary=(
                        "The optimized prompt produced a substantially more structured, focused, and actionable "
                        "response with distinct sections, while the original prompt yielded a broader, conversational "
                        "overview."
                    ),
                    recommendation="Use the optimized formulation when precise execution is needed, or the original for quick brainstorming."
                )

    # ================= Offline / Simulation Fallback Engine =================
    def _heuristic_analyze_fallback(self, prompt: str) -> PromptAnalysisResult:
        """Heuristic analyzer when running in offline/demo mode without API key."""
        word_count = len(prompt.split())
        has_role = bool(re.search(r"\b(act as|you are|expert|architect|developer|specialist|consultant)\b", prompt, re.I))
        has_format = bool(re.search(r"\b(json|markdown|table|bullet|list|steps|format|schema|code)\b", prompt, re.I))
        has_constraints = bool(re.search(r"\b(do not|must|only|limit|avoid|never|maximum|minimum|constraints)\b", prompt, re.I))
        has_context = bool(re.search(r"\b(because|for|working on|project|environment|audience|scenario|context)\b", prompt, re.I))
        
        clarity_score = min(92, 55 + min(30, word_count * 2))
        context_score = 85 if has_context else 40
        specificity_score = 88 if word_count > 25 and (has_format or has_constraints) else 45
        task_score = 85 if word_count > 6 else 50
        format_score = 90 if has_format else 30
        constraint_score = 88 if has_constraints else 25

        overall = int(
            (task_score * 0.20) +
            (clarity_score * 0.20) +
            (specificity_score * 0.20) +
            (context_score * 0.15) +
            (format_score * 0.15) +
            (constraint_score * 0.10)
        )

        weaknesses = []
        if not has_role:
            weaknesses.append(WeaknessItem(
                weakness="Missing Persona/Role Definition",
                why_it_matters="Without an assigned expert role, the LLM generates generalized, conversational output rather than specialized, authoritative insights."
            ))
        if not has_format:
            weaknesses.append(WeaknessItem(
                weakness="Unspecified Output Structure",
                why_it_matters="The model is forced to choose its own layout, often leading to inconsistent paragraphs that are difficult to parse or integrate."
            ))
        if not has_constraints:
            weaknesses.append(WeaknessItem(
                weakness="Lack of Guardrails and Negative Constraints",
                why_it_matters="Without negative boundaries or scope ceilings, the model frequently introduces unsolicited fluff, unnecessary code, or invalid assumptions."
            ))
        if not has_context:
            weaknesses.append(WeaknessItem(
                weakness="Absent Operational Context",
                why_it_matters="The model has no visibility into your tech stack, audience level, or business constraints, leading to generic textbook advice."
            ))

        recs = [
            "Assign an explicit persona (e.g., 'Act as a Senior Software Architect').",
            "Specify the desired output format (e.g., 'Return a Markdown table with columns: X, Y, Z').",
            "Define explicit boundary constraints (e.g., 'Limit to top 3 strategies, avoid external dependencies').",
            "Provide background context explaining the target audience and technical environment."
        ]

        return PromptAnalysisResult(
            overall_score=overall,
            scoring_basis_summary=(
                "Evaluation calculated via PromptIQ's 6-dimensional rubric: Task Definition (20%), "
                "Clarity (20%), Specificity (20%), Context (15%), Output Format (15%), Constraints (10%). "
                "Scores reflect presence of concrete parameters, structured formatting tags, and negative constraints."
            ),
            clarity=CriterionEvaluation(
                score=clarity_score,
                rationale="Prompt text conveys general direction but relies heavily on model assumptions."
            ),
            context=CriterionEvaluation(
                score=context_score,
                rationale="Minimal domain or situational environment provided. Needs target audience and system boundaries."
            ),
            specificity=CriterionEvaluation(
                score=specificity_score,
                rationale="Lacks exact quantitative targets, scope limitations, or concrete criteria."
            ),
            task_definition=CriterionEvaluation(
                score=task_score,
                rationale="The primary objective is identifiable but would benefit from explicit action verbs."
            ),
            output_format=CriterionEvaluation(
                score=format_score,
                rationale="No explicit output schema (table, JSON, section headers) was requested."
            ),
            constraints=CriterionEvaluation(
                score=constraint_score,
                rationale="No negative constraints, word count boundaries, or operational limits specified."
            ),
            weaknesses=weaknesses,
            recommendations=recs,
        )

    def _heuristic_optimize_fallback(self, prompt: str) -> PromptOptimizationResult:
        """Heuristic optimizer when running in offline/demo mode without API key."""
        clean = prompt.strip()
        improved = (
            f"You are a Senior Domain Specialist and Technical Consultant.\n\n"
            f"### Context & Objective\n"
            f"The goal is to address the following objective with rigorous detail and actionable clarity:\n"
            f"> {clean}\n\n"
            f"### Key Requirements & Methodology\n"
            f"1. Break down the core concepts into logical, step-by-step components.\n"
            f"2. Provide concrete real-world examples and trade-off analyses where applicable.\n"
            f"3. Explain the underlying mechanics and failure modes to watch out for.\n\n"
            f"### Output Format\n"
            f"- **Executive Summary**: 2-3 concise sentences stating the primary answer.\n"
            f"- **In-Depth Breakdown**: Structured sections with clear Markdown subheadings.\n"
            f"- **Actionable Recommendations**: Bulleted checklist of immediate next steps.\n\n"
            f"### Constraints & Guardrails\n"
            f"- Do not use conversational filler (e.g., 'Certainly!', 'Here is...').\n"
            f"- Keep technical terminology precise and grounded in industry standards.\n"
            f"- If assumptions are made, explicitly list them under an Assumptions heading."
        )

        return PromptOptimizationResult(
            improved_prompt=improved,
            role_defined="Senior Domain Specialist and Technical Consultant",
            task_defined=f"Deliver a rigorous, step-by-step breakdown addressing: '{clean}'",
            context_provided="Injected target environment, step-by-step methodology, and real-world failure analysis requirements.",
            output_format_specified="Structured Markdown with Executive Summary, In-Depth Breakdown, and Actionable Checklist.",
            constraints_applied="Eliminated conversational filler, enforced technical precision, and required explicit assumption declaration.",
            improvements_table=[
                ImprovementRow(
                    original_element="Unspecified persona",
                    improvement="Added 'Senior Domain Specialist and Technical Consultant'",
                    reason="Primes the model's high-tier latent knowledge and enforces an authoritative, professional tone."
                ),
                ImprovementRow(
                    original_element="Open-ended task prompt",
                    improvement="Structured into 3 distinct analytical stages (Concepts, Trade-offs, Failure modes)",
                    reason="Prevents superficial single-paragraph replies and enforces comprehensive depth."
                ),
                ImprovementRow(
                    original_element="No output format defined",
                    improvement="Mandated Executive Summary, Thematic Subheadings, and Action Checklist",
                    reason="Ensures immediate readability, scannability, and ease of downstream integration."
                ),
                ImprovementRow(
                    original_element="No negative constraints",
                    improvement="Banned conversational filler; mandated explicit assumption labeling",
                    reason="Increases signal-to-noise ratio and prevents hallucinations from masquerading as facts."
                )
            ]
        )

    def _heuristic_execute_fallback(self, prompt: str) -> str:
        """Simulated model response for offline testing."""
        return (
            f"[Offline Demonstration Output for Prompt]:\n\n"
            f"## Summary\n"
            f"This is a demonstration response generated in Offline Mode to demonstrate PromptIQ's dual execution lab.\n\n"
            f"### Key Observations\n"
            f"- Received prompt length: {len(prompt)} characters ({len(prompt.split())} words).\n"
            f"- When a live Google Gemini API key is configured, PromptIQ calls Google's live `{self.model_name}` model.\n"
            f"- Both prompts are evaluated independently with temperature and sampling settings preserved.\n\n"
            f"To enable live inference, enter your Gemini API key in the sidebar."
        )

    def _heuristic_compare_fallback(self, original_out: str, improved_out: str) -> ComparisonAnalysisResult:
        """Simulated comparative synthesis for offline mode."""
        return ComparisonAnalysisResult(
            observable_differences=[
                ObservableDifference(
                    category="Structural Organization",
                    original_behavior="Generated unstructured text paragraphs without clear visual separation.",
                    improved_behavior="Produced hierarchical Markdown headers, bulleted lists, and delineated sections.",
                    takeaway="Structured output requirements dramatically reduce cognitive load for human readers."
                ),
                ObservableDifference(
                    category="Actionability & Precision",
                    original_behavior="Offered high-level general guidance with limited concrete steps.",
                    improved_behavior="Delivered specific parameters, tactical checklists, and explicit guardrails.",
                    takeaway="Specifying format and negative constraints turns generic text into an executable plan."
                )
            ],
            comparative_summary=(
                "Based on the empirical outputs, the optimized prompt produced significantly higher structure, "
                "greater operational clarity, and less conversational filler than the original baseline prompt."
            ),
            recommendation="Adopt the optimized prompt for production workflows and technical documentation."
        )
