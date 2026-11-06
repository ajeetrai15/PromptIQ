"""Automated test suite verifying PromptIQ core logic, schemas, and fallback engines."""

import unittest
from core.schemas import (
    PromptAnalysisResult,
    PromptOptimizationResult,
    ComparisonAnalysisResult,
    CriterionEvaluation,
    WeaknessItem,
    ImprovementRow,
    ObservableDifference,
)
from core.gemini_service import GeminiService
from core.analyzer import analyze_prompt
from core.optimizer import optimize_prompt
from core.comparator import run_comparison
from data.templates import TEMPLATES, get_categories, get_templates_by_category
from data.education import EDUCATIONAL_TOPICS


class TestPromptIQ(unittest.TestCase):
    """Unit and functional tests for PromptIQ."""

    def test_schema_validation(self):
        """Verify Pydantic models validate correctly."""
        analysis = PromptAnalysisResult(
            overall_score=75,
            scoring_basis_summary="Weighted rubric score based on 6 key dimensions.",
            clarity=CriterionEvaluation(score=80, rationale="Clear statement of goal"),
            context=CriterionEvaluation(score=60, rationale="Missing tech stack info"),
            specificity=CriterionEvaluation(score=70, rationale="Reasonable detail"),
            task_definition=CriterionEvaluation(score=85, rationale="Primary task is evident"),
            output_format=CriterionEvaluation(score=65, rationale="Format implied but not strictly bounded"),
            constraints=CriterionEvaluation(score=60, rationale="Few constraints set"),
            weaknesses=[WeaknessItem(weakness="No negative constraints", why_it_matters="Model may add filler")],
            recommendations=["Add role and explicit schema"],
        )
        self.assertEqual(analysis.overall_score, 75)
        self.assertEqual(len(analysis.weaknesses), 1)
        self.assertEqual(analysis.clarity.score, 80)

    def test_heuristic_analyzer_fallback(self):
        """Verify prompt analyzer offline heuristic engine runs and produces valid scores."""
        service = GeminiService(force_offline=True)
        res = service._heuristic_analyze_fallback("Explain quantum computing and how qubits work.")
        
        self.assertIsInstance(res, PromptAnalysisResult)
        self.assertGreaterEqual(res.overall_score, 0)
        self.assertLessEqual(res.overall_score, 100)
        self.assertIn("Scoring Basis:", "Scoring Basis:" if res.scoring_basis_summary else "")
        self.assertGreater(len(res.weaknesses), 0)
        self.assertGreater(len(res.recommendations), 0)

        # Check all 6 criteria are scored
        criteria = [res.clarity, res.context, res.specificity, res.task_definition, res.output_format, res.constraints]
        for c in criteria:
            self.assertGreaterEqual(c.score, 0)
            self.assertLessEqual(c.score, 100)
            self.assertTrue(len(c.rationale) > 5)

    def test_heuristic_optimizer_fallback(self):
        """Verify prompt optimizer creates structured prompt with table breakdown."""
        service = GeminiService(force_offline=True)
        raw_prompt = "Write a Python script to scrape product prices."
        res = service._heuristic_optimize_fallback(raw_prompt)

        self.assertIsInstance(res, PromptOptimizationResult)
        self.assertIn(raw_prompt, res.improved_prompt)
        self.assertTrue(len(res.role_defined) > 0)
        self.assertTrue(len(res.output_format_specified) > 0)
        self.assertTrue(len(res.constraints_applied) > 0)
        self.assertGreater(len(res.improvements_table), 0)
        for row in res.improvements_table:
            self.assertTrue(len(row.original_element) > 0)
            self.assertTrue(len(row.improvement) > 0)
            self.assertTrue(len(row.reason) > 0)

    def test_comparator_fallback(self):
        """Verify comparison lab executes dual outputs and synthesizes observable differences."""
        service = GeminiService(force_offline=True)
        orig_out, opt_out, comp_res = run_comparison(
            original_prompt="Summarize quantum computing.",
            improved_prompt="Act as a physicist and summarize quantum computing in a Markdown table.",
            temperature=0.5,
            service=service,
        )

        self.assertTrue(len(orig_out) > 0)
        self.assertTrue(len(opt_out) > 0)
        self.assertIsInstance(comp_res, ComparisonAnalysisResult)
        self.assertGreater(len(comp_res.observable_differences), 0)
        self.assertTrue(len(comp_res.comparative_summary) > 0)
        self.assertTrue(len(comp_res.recommendation) > 0)

    def test_templates_coverage(self):
        """Verify all 6 required categories are present in template library."""
        expected_categories = [
            "Learning",
            "Coding",
            "Research",
            "Content writing",
            "Data analysis",
            "Interview preparation",
        ]
        categories = get_categories()
        for cat in expected_categories:
            self.assertIn(cat, categories, f"Category {cat} should be present in templates.")
            tpls = get_templates_by_category(cat)
            self.assertGreaterEqual(len(tpls), 2, f"Category {cat} should have at least 2 templates.")

    def test_educational_topics_coverage(self):
        """Verify all required educational concepts are explained, including chain-of-thought caveat."""
        required_topics = [
            "role_prompting",
            "context",
            "specificity",
            "constraints",
            "output_formatting",
            "few_shot",
            "chain_of_thought",
        ]
        topic_ids = [t["id"] for t in EDUCATIONAL_TOPICS]
        for req in required_topics:
            self.assertIn(req, topic_ids, f"Educational topic {req} missing.")

        cot = next(t for t in EDUCATIONAL_TOPICS if t["id"] == "chain_of_thought")
        self.assertIn("concise reasoning summaries or key intermediate steps", cot["best_practices"][0].lower())

    def test_empty_prompt_error_handling(self):
        """Verify empty input raises ValueError gracefully."""
        with self.assertRaises(ValueError):
            analyze_prompt("")
        with self.assertRaises(ValueError):
            optimize_prompt("   ")
        with self.assertRaises(ValueError):
            run_comparison("", "improved")
        with self.assertRaises(ValueError):
            run_comparison("original", "   ")

    def test_history_and_state_management(self):
        """Verify session state history addition, limits, and clearing."""
        import streamlit as st
        from utils.state import init_session_state, add_to_history, clear_history, load_prompt_into, sync_navigation

        init_session_state()
        self.assertEqual(len(st.session_state.history), 0)

        # Add items
        add_to_history("Prompt 1", "Analyzer", {"score": 85})
        add_to_history("Prompt 2", "Optimizer", {})
        self.assertEqual(len(st.session_state.history), 2)
        self.assertEqual(st.session_state.history[0]["prompt"], "Prompt 2")

        # Duplicate consecutive check
        add_to_history("Prompt 2", "Optimizer", {})
        self.assertEqual(len(st.session_state.history), 2)

        # Load prompt helper
        load_prompt_into("Target Prompt", "✨ Prompt Optimizer", "Target Opt")
        self.assertEqual(st.session_state.current_prompt, "Target Prompt")
        self.assertEqual(st.session_state.optimized_prompt, "Target Opt")
        self.assertEqual(st.session_state.navigation_page, "✨ Prompt Optimizer")
        self.assertEqual(st.session_state.target_nav_page, "✨ Prompt Optimizer")

        # Synchronize navigation before widget instantiation
        sync_navigation()
        self.assertEqual(st.session_state.nav_radio, "✨ Prompt Optimizer")
        self.assertIsNone(st.session_state.target_nav_page)

        # Clear history
        clear_history()
        self.assertEqual(len(st.session_state.history), 0)

    def test_navigation_widget_decoupling_regression(self):
        """Regression test ensuring load_prompt_into does not modify widget-instantiated keys directly."""
        import streamlit as st
        from utils.state import init_session_state, load_prompt_into, sync_navigation

        init_session_state()

        # Simulate existing instantiated widget state
        st.session_state.nav_radio = "🔬 Prompt Analyzer"
        st.session_state.navigation_page = "🔬 Prompt Analyzer"

        # Action: User on analyzer page clicks "Upgrade Your Prompt"
        analyzed_prompt = "Write a Python script to scrape products."
        load_prompt_into(analyzed_prompt, "✨ Prompt Optimizer")

        # Verify: current_prompt is immediately transferred for the optimizer view
        self.assertEqual(st.session_state.current_prompt, analyzed_prompt)
        self.assertEqual(st.session_state.navigation_page, "✨ Prompt Optimizer")
        self.assertEqual(st.session_state.target_nav_page, "✨ Prompt Optimizer")

        # Verify: nav_radio was NOT mutated during load_prompt_into (prevents StreamlitWidgetAlreadyInstantiatedError)
        self.assertEqual(st.session_state.nav_radio, "🔬 Prompt Analyzer")

        # Next run pass: app.py runs sync_navigation before st.radio instantiation
        nav_options = [
            "🔬 Prompt Analyzer",
            "✨ Prompt Optimizer",
            "⚖️ Comparison Lab",
            "📚 Prompt Templates",
            "🎓 Educational Academy",
            "🕒 History & Vault",
        ]
        active_page = sync_navigation(nav_options)

        # After safe pre-widget sync:
        self.assertEqual(active_page, "✨ Prompt Optimizer")
        self.assertEqual(st.session_state.nav_radio, "✨ Prompt Optimizer")
        self.assertEqual(st.session_state.navigation_page, "✨ Prompt Optimizer")
        self.assertIsNone(st.session_state.target_nav_page)


if __name__ == "__main__":
    unittest.main()
