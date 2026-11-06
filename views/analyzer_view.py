"""Prompt Analyzer View for multi-dimensional diagnostic evaluation."""

import streamlit as st
from core.analyzer import analyze_prompt
from core.gemini_service import GeminiService
from utils.state import add_to_history, load_prompt_into
from utils.ui_helpers import render_metric_card, render_score_badge, render_empty_state


def render_analyzer_view():
    st.subheader("🔬 Prompt Quality Diagnostic")
    st.caption("Evaluate your prompt against 6 fundamental dimensions of prompt engineering with objective scoring and flaw analysis.")

    # Input Area
    user_prompt = st.text_area(
        "Enter Prompt to Analyze:",
        value=st.session_state.current_prompt,
        height=140,
        placeholder="e.g. Write a python script to scrape products from an e-commerce page...",
        help="Paste any AI prompt here to receive an in-depth rubric evaluation.",
    )

    col_btn, col_actions = st.columns([1, 2])
    with col_btn:
        analyze_clicked = st.button("🚀 Analyze Prompt", type="primary", use_container_width=True)

    with col_actions:
        sample_choice = st.selectbox(
            "Or load a sample weak prompt:",
            [
                "-- Select a sample --",
                "Explain how machine learning works.",
                "Write a blog post about our SaaS tool.",
                "Help me fix my slow database query.",
                "Prepare me for a job interview.",
            ],
            label_visibility="collapsed",
        )
        if sample_choice != "-- Select a sample --" and sample_choice != user_prompt:
            st.session_state.current_prompt = sample_choice
            st.rerun()

    if analyze_clicked:
        if not user_prompt.strip():
            st.warning("⚠️ Please enter a prompt to analyze.")
            return

        with st.spinner("Analyzing prompt architecture and linguistic constraints..."):
            try:
                service = GeminiService(
                    api_key=st.session_state.api_key,
                    model_name=st.session_state.selected_model,
                )
                result = analyze_prompt(user_prompt, service=service)
                st.session_state.analysis_result = result
                st.session_state.current_prompt = user_prompt

                # Record in history
                add_to_history(
                    prompt=user_prompt,
                    action_type="Analyzer",
                    details={
                        "overall_score": result.overall_score,
                        "clarity": result.clarity.score,
                        "context": result.context.score,
                        "specificity": result.specificity.score,
                    },
                )
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                return

    # Render Results if available
    res = st.session_state.analysis_result
    if res:
        st.markdown("---")
        
        # Overall Score Banner
        st.markdown(
            f"""
            <div class="piq-metric-card" style="border-left: 6px solid #6366F1; padding: 1.25rem 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <div style="font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Overall Prompt IQ Score</div>
                        <div style="font-size: 2.4rem; font-weight: 800;">{res.overall_score} <span style="font-size: 1.2rem; color: #64748B;">/ 100</span></div>
                    </div>
                    <div>
                        {render_score_badge(res.overall_score)}
                    </div>
                </div>
                <div style="margin-top: 0.8rem; font-size: 0.9rem; color: #CBD5E1; line-height: 1.45;">
                    <strong>Scoring Basis:</strong> {res.scoring_basis_summary}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### 📊 Evaluation Rubric Breakdown")
        col1, col2 = st.columns(2)

        with col1:
            render_metric_card("1. Clarity", res.clarity.score, res.clarity.rationale)
            render_metric_card("2. Context", res.context.score, res.context.rationale)
            render_metric_card("3. Specificity", res.specificity.score, res.specificity.rationale)

        with col2:
            render_metric_card("4. Task Definition", res.task_definition.score, res.task_definition.rationale)
            render_metric_card("5. Output Format", res.output_format.score, res.output_format.rationale)
            render_metric_card("6. Constraints", res.constraints.score, res.constraints.rationale)

        # Weaknesses
        st.markdown("#### ⚠️ Detected Flaws & Why They Matter")
        if res.weaknesses:
            for w in res.weaknesses:
                st.markdown(
                    f"""
                    <div class="piq-weakness-card">
                        <div class="piq-weakness-title">⚡ {w.weakness}</div>
                        <div class="piq-weakness-impact"><strong>Impact:</strong> {w.why_it_matters}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.success("🎉 No significant architectural flaws detected in this prompt!")

        # Recommendations
        st.markdown("#### 💡 Actionable Recommendations")
        for idx, rec in enumerate(res.recommendations, 1):
            st.markdown(f"- **{rec}**")

        # Next Step Bridge Actions
        st.markdown("---")
        st.markdown("##### 🚀 Next Step: Upgrade Your Prompt")
        col_opt, col_lab = st.columns(2)
        with col_opt:
            st.button(
                "✨ Upgrade Your Prompt",
                key="btn_upgrade_prompt_optimizer",
                on_click=load_prompt_into,
                args=(user_prompt, "✨ Prompt Optimizer"),
                use_container_width=True,
                help="Transfer this analyzed prompt to the Prompt Optimizer for architectural enhancement.",
            )
        with col_lab:
            st.button(
                "⚖️ Test in Comparison Lab",
                key="btn_test_comparison_lab",
                on_click=load_prompt_into,
                args=(user_prompt, "⚖️ Comparison Lab"),
                use_container_width=True,
                help="Transfer this prompt into the Comparison Lab to run dual inference.",
            )
    else:
        render_empty_state(
            title="No Prompt Analyzed Yet",
            message="Enter a prompt above or select a sample to inspect its quality scores, flaws, and recommendations.",
        )
