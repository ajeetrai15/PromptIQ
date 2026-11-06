"""Prompt Comparison Lab View for side-by-side Gemini inference and empirical output analysis."""

import streamlit as st
from core.comparator import run_comparison
from core.optimizer import optimize_prompt
from core.gemini_service import GeminiService
from utils.state import add_to_history
from utils.ui_helpers import render_empty_state


def render_comparator_view():
    st.subheader("⚖️ Empirical Comparison Lab")
    st.caption("Execute both prompts side-by-side using Gemini, compare actual responses, and review empirical differences without bias.")

    # Two-column layout for input prompts
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("##### 📝 Original Prompt")
        orig_prompt = st.text_area(
            "Original Prompt:",
            value=st.session_state.current_prompt,
            height=160,
            placeholder="Enter baseline prompt...",
            label_visibility="collapsed",
            key="comp_orig_input",
        )

    with col_p2:
        st.markdown("##### ⚡ Optimized Prompt")
        opt_prompt = st.text_area(
            "Optimized Prompt:",
            value=st.session_state.optimized_prompt,
            height=160,
            placeholder="Enter optimized prompt or click 'Auto-Generate' below...",
            label_visibility="collapsed",
            key="comp_opt_input",
        )

    # Action Toolbar
    col_run, col_gen, col_temp = st.columns([1.5, 1.5, 1])

    with col_gen:
        if st.button("🪄 Auto-Generate Optimized Prompt", use_container_width=True):
            if not orig_prompt.strip():
                st.warning("⚠️ Enter an original prompt first.")
            else:
                with st.spinner("Engineering optimized prompt..."):
                    try:
                        srv = GeminiService(
                            api_key=st.session_state.api_key,
                            model_name=st.session_state.selected_model,
                        )
                        res = optimize_prompt(orig_prompt, service=srv)
                        st.session_state.current_prompt = orig_prompt
                        st.session_state.optimized_prompt = res.improved_prompt
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Optimization failed: {e}")

    with col_temp:
        temp_val = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="Sampling randomness for both generations.")

    with col_run:
        run_clicked = st.button("🚀 Run Dual Test with Gemini", type="primary", use_container_width=True)

    if run_clicked:
        if not orig_prompt.strip():
            st.warning("⚠️ Please provide an Original Prompt.")
            return
        if not opt_prompt.strip():
            st.warning("⚠️ Please provide or generate an Optimized Prompt.")
            return

        with st.spinner(f"Running dual inference against Gemini ({st.session_state.selected_model}) and analyzing output variance..."):
            try:
                srv = GeminiService(
                    api_key=st.session_state.api_key,
                    model_name=st.session_state.selected_model,
                )
                orig_out, opt_out, comp_analysis = run_comparison(
                    original_prompt=orig_prompt,
                    improved_prompt=opt_prompt,
                    temperature=temp_val,
                    service=srv,
                )

                st.session_state.comparison_result = {
                    "orig_prompt": orig_prompt,
                    "opt_prompt": opt_prompt,
                    "orig_out": orig_out,
                    "opt_out": opt_out,
                    "analysis": comp_analysis,
                }

                # Record in history
                add_to_history(
                    prompt=orig_prompt,
                    action_type="Comparison Lab",
                    details={"model": st.session_state.selected_model, "temp": temp_val},
                )
            except Exception as e:
                st.error(f"❌ Comparison execution failed: {str(e)}")
                return

    # Display Dual Outputs and Empirical Analysis
    comp_data = st.session_state.comparison_result
    if comp_data:
        st.markdown("---")
        st.markdown("#### 💬 Dual Model Generation Outputs")

        col_out1, col_out2 = st.columns(2)

        with col_out1:
            st.markdown(
                """
                <div style="background-color: rgba(30, 41, 59, 0.4); padding: 0.5rem 0.8rem; border-radius: 6px; margin-bottom: 0.5rem; font-weight: 600;">
                    📝 Original Prompt Output
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(comp_data["orig_out"])
            st.caption(f"Tokens/Length: ~{len(comp_data['orig_out'].split())} words")

        with col_out2:
            st.markdown(
                """
                <div style="background-color: rgba(79, 70, 229, 0.15); border: 1px solid rgba(79, 70, 229, 0.3); padding: 0.5rem 0.8rem; border-radius: 6px; margin-bottom: 0.5rem; font-weight: 600; color: #818CF8;">
                    ⚡ Optimized Prompt Output
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(comp_data["opt_out"])
            st.caption(f"Tokens/Length: ~{len(comp_data['opt_out'].split())} words")

        # Empirical Comparison Analysis
        st.markdown("---")
        st.markdown("#### 🔬 Empirical Difference Analysis")
        st.caption("Objective breakdown of observable variances between both responses without subjective assumptions:")

        analysis = comp_data["analysis"]

        # Comparative Summary Card
        st.markdown(
            f"""
            <div class="piq-metric-card" style="border-left: 5px solid #38BDF8;">
                <div class="piq-metric-title">Comparative Synthesis</div>
                <div style="font-size: 0.95rem; color: #F1F5F9; line-height: 1.5; margin-bottom: 0.5rem;">
                    {analysis.comparative_summary}
                </div>
                <div style="font-size: 0.88rem; color: #94A3B8;">
                    <strong>Practical Takeaway:</strong> {analysis.recommendation}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Observable differences table / cards
        st.markdown("##### 🔍 Observed Dimensions of Variance")
        for diff in analysis.observable_differences:
            with st.expander(f"📌 {diff.category}", expanded=True):
                c_d1, c_d2 = st.columns(2)
                with c_d1:
                    st.markdown("**Original Response Pattern:**")
                    st.markdown(f"*{diff.original_behavior}*")
                with c_d2:
                    st.markdown("**Optimized Response Pattern:**")
                    st.markdown(f"*{diff.improved_behavior}*")
                st.info(f"💡 **Why This Occurred:** {diff.takeaway}")

    else:
        render_empty_state(
            title="Comparison Lab Ready",
            message="Enter an original prompt and optimized prompt above, then click 'Run Dual Test with Gemini' to execute both and analyze empirical outputs.",
        )
