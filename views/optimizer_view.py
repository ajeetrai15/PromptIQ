"""Prompt Optimizer View with side-by-side prompt diffs and explanation table."""

import pandas as pd
import streamlit as st
from core.optimizer import optimize_prompt
from core.gemini_service import GeminiService
from utils.state import add_to_history, load_prompt_into
from utils.ui_helpers import render_empty_state


def render_optimizer_view():
    st.subheader("✨ Prompt Optimizer & Engineering Studio")
    st.caption("Transform vague, open-ended prompts into production-grade prompts with injected roles, context, formatting, and constraints.")

    # Input Area
    user_prompt = st.text_area(
        "Original Prompt to Optimize:",
        value=st.session_state.current_prompt,
        height=120,
        placeholder="e.g. Write a customer retention email...",
        help="Input your baseline prompt. PromptIQ will rewrite it while preserving your core objective.",
    )

    col_btn, col_sample = st.columns([1, 2])
    with col_btn:
        opt_clicked = st.button("🪄 Optimize Prompt", type="primary", use_container_width=True)

    with col_sample:
        sample_opt = st.selectbox(
            "Or pick an unoptimized example:",
            [
                "-- Select an unoptimized example --",
                "Explain quantum computing and how qubits work.",
                "Write a Python script to scrape product prices from an e-commerce page.",
                "Write a blog post announcing our new developer API gateway.",
                "How do I analyze customer churn for my subscription app?",
                "Prepare me for a system design interview about designing a rate limiter.",
            ],
            label_visibility="collapsed",
        )
        if sample_opt != "-- Select an unoptimized example --" and sample_opt != user_prompt:
            st.session_state.current_prompt = sample_opt
            st.rerun()

    if opt_clicked:
        if not user_prompt.strip():
            st.warning("⚠️ Please provide a prompt to optimize.")
            return

        with st.spinner("Refactoring prompt with architectural role, context, schemas, and guardrails..."):
            try:
                service = GeminiService(
                    api_key=st.session_state.api_key,
                    model_name=st.session_state.selected_model,
                )
                res = optimize_prompt(user_prompt, service=service)
                st.session_state.optimization_result = res
                st.session_state.current_prompt = user_prompt
                st.session_state.optimized_prompt = res.improved_prompt

                # Record in history
                add_to_history(
                    prompt=user_prompt,
                    action_type="Optimizer",
                    details={"improved_prompt": res.improved_prompt},
                )
            except Exception as e:
                st.error(f"❌ Optimization failed: {str(e)}")
                return

    # Display Side-by-Side and Changes
    opt_res = st.session_state.optimization_result
    if opt_res:
        st.markdown("---")
        st.markdown("#### 🔄 Side-by-Side Prompt Comparison")

        col_orig, col_opt = st.columns(2)
        with col_orig:
            st.markdown("##### 📝 Original Prompt")
            st.info(user_prompt)
            st.caption(f"Length: {len(user_prompt)} chars • {len(user_prompt.split())} words")

        with col_opt:
            st.markdown("##### ⚡ Engineered & Optimized Prompt")
            st.success(opt_res.improved_prompt)
            st.caption(f"Length: {len(opt_res.improved_prompt)} chars • {len(opt_res.improved_prompt.split())} words")

        # Copy / Export Code Area
        with st.expander("📋 View Clean Copyable Markdown Block"):
            st.code(opt_res.improved_prompt, language="markdown")

        # Architectural Injections Summary Cards
        st.markdown("#### 🧩 Engineered Components Injected")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f"""
                <div class="piq-metric-card">
                    <div class="piq-metric-title">🎭 Injected Role / Persona</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #E2E8F0;">{opt_res.role_defined}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""
                <div class="piq-metric-card">
                    <div class="piq-metric-title">📐 Output Format Specification</div>
                    <div style="font-size: 0.88rem; color: #CBD5E1;">{opt_res.output_format_specified}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f"""
                <div class="piq-metric-card">
                    <div class="piq-metric-title">🛡️ Guardrails & Constraints</div>
                    <div style="font-size: 0.88rem; color: #CBD5E1;">{opt_res.constraints_applied}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 3. Prompt Improvement Explanation Table
        st.markdown("#### 📋 Prompt Improvement Explanation")
        st.caption("Granular mapping of original weaknesses to applied improvements and underlying prompt engineering rationale:")

        if opt_res.improvements_table:
            table_data = [
                {
                    "Original Element": row.original_element,
                    "Improvement": row.improvement,
                    "Reason": row.reason,
                }
                for row in opt_res.improvements_table
            ]
            df = pd.DataFrame(table_data)
            st.table(df)

        # Bridge Action to Comparison Lab
        st.markdown("---")
        st.markdown("##### 🔬 Ready to test this in practice?")
        st.button(
            "⚖️ Run Both Prompts in Comparison Lab",
            key="btn_opt_to_comparison_lab",
            on_click=load_prompt_into,
            args=(user_prompt, "⚖️ Comparison Lab", opt_res.improved_prompt),
            type="primary",
            use_container_width=True,
            help="Transfer both original and optimized prompts into the Comparison Lab.",
        )

    else:
        render_empty_state(
            title="No Optimization Performed Yet",
            message="Enter a prompt above or pick a sample to view side-by-side prompt optimization and the detailed changes explanation table.",
        )
