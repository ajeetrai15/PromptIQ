"""Prompt History View for inspecting, reusing, and clearing past session runs."""

import streamlit as st
from utils.state import clear_history, load_prompt_into
from utils.ui_helpers import render_empty_state


def render_history_view():
    st.subheader("🕒 Session History & Prompt Vault")
    st.caption("Review, inspect, and reuse prompts evaluated or generated during your current session.")

    history = st.session_state.history

    if not history:
        render_empty_state(
            title="No Session History Yet",
            message="Prompts tested in the Analyzer, Optimizer, or Comparison Lab will automatically appear here for rapid recall and reuse.",
        )
        return

    col_info, col_clear = st.columns([3, 1])
    with col_info:
        st.markdown(f"**Total Tracked Runs:** {len(history)}")
    with col_clear:
        if st.button("🗑️ Clear History", type="secondary", use_container_width=True):
            clear_history()
            st.rerun()

    st.markdown("---")

    for idx, item in enumerate(history):
        action = item.get("action_type", "General")
        ts = item.get("timestamp", "")
        prompt = item.get("prompt", "")
        details = item.get("details", {})

        with st.container():
            st.markdown(
                f"""
                <div class="piq-metric-card" style="margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                        <span class="piq-badge piq-badge-neutral">{action}</span>
                        <span style="font-size: 0.8rem; color: #64748B;">{ts}</span>
                    </div>
                    <div style="font-size: 0.95rem; color: #F1F5F9; font-family: monospace; white-space: pre-wrap; margin-bottom: 0.5rem;">{prompt}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Metadata details if any
            if "overall_score" in details:
                st.caption(f"Score: {details['overall_score']}/100 | Clarity: {details.get('clarity')} | Specificity: {details.get('specificity')}")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"🔬 Analyze Again", key=f"hist_an_{item['id']}", use_container_width=True):
                    load_prompt_into(prompt, "🔬 Prompt Analyzer")
                    st.rerun()
            with col2:
                if st.button(f"✨ Optimize", key=f"hist_opt_{item['id']}", use_container_width=True):
                    opt_val = details.get("improved_prompt", "")
                    load_prompt_into(prompt, "✨ Prompt Optimizer", optimized_text=opt_val)
                    st.rerun()
            with col3:
                if st.button(f"⚖️ Compare in Lab", key=f"hist_cmp_{item['id']}", use_container_width=True):
                    opt_val = details.get("improved_prompt", "")
                    load_prompt_into(prompt, "⚖️ Comparison Lab", optimized_text=opt_val)
                    st.rerun()

            st.markdown("<div style='margin-bottom: 0.75rem;'></div>", unsafe_allow_html=True)
