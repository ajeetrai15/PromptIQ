"""Prompt Templates View with domain categorization and one-click loader."""

import streamlit as st
from data.templates import TEMPLATES, get_categories
from utils.state import load_prompt_into


def render_templates_view():
    st.subheader("📚 Prompt Engineering Template Library")
    st.caption("Explore realistic prompts across 6 core professional domains, understand their latent flaws, and load them directly into laboratory tools.")

    # Filter toolbar
    categories = ["All"] + get_categories()
    col_cat, col_search = st.columns([1, 2])
    with col_cat:
        selected_category = st.selectbox("Filter Category:", categories)
    with col_search:
        search_query = st.text_input("Search Templates:", placeholder="Search by title, prompt keywords, or domain...")

    # Filtered List
    filtered = TEMPLATES
    if selected_category != "All":
        filtered = [t for t in filtered if t["category"].lower() == selected_category.lower()]
    if search_query.strip():
        q = search_query.strip().lower()
        filtered = [
            t for t in filtered
            if q in t["title"].lower() or q in t["prompt"].lower() or q in t["description"].lower()
        ]

    st.markdown(f"Showing **{len(filtered)}** template(s):")

    for t in filtered:
        with st.container():
            st.markdown(
                f"""
                <div class="piq-metric-card" style="margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <span style="font-size: 1.1rem; font-weight: 700; color: #F8FAFC;">{t['title']}</span>
                        <span class="piq-badge piq-badge-neutral">{t['category']}</span>
                    </div>
                    <div style="color: #94A3B8; font-size: 0.9rem; margin-bottom: 0.6rem;">{t['description']}</div>
                    <div style="background-color: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 6px; padding: 0.75rem 1rem; font-family: monospace; font-size: 0.92rem; color: #E2E8F0; margin-bottom: 0.6rem;">
                        "{t['prompt']}"
                    </div>
                    <div style="font-size: 0.85rem; color: #F59E0B; margin-bottom: 0.6rem;">
                        <strong>⚠️ Common Flaws:</strong> {t['notes']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🔬 Analyze Prompt", key=f"tpl_an_{t['id']}", use_container_width=True):
                    load_prompt_into(t["prompt"], "🔬 Prompt Analyzer")
                    st.rerun()
            with c2:
                if st.button("✨ Optimize Prompt", key=f"tpl_opt_{t['id']}", use_container_width=True):
                    load_prompt_into(t["prompt"], "✨ Prompt Optimizer")
                    st.rerun()
            with c3:
                if st.button("⚖️ Compare in Lab", key=f"tpl_cmp_{t['id']}", use_container_width=True):
                    load_prompt_into(t["prompt"], "⚖️ Comparison Lab")
                    st.rerun()
            
            st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
