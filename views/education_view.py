"""Educational Mode View with clear explanations of core prompt engineering paradigms."""

import streamlit as st
from data.education import EDUCATIONAL_TOPICS
from utils.state import load_prompt_into


def render_education_view():
    st.subheader("🎓 Prompt Engineering Academy & Guide")
    st.caption("Master fundamental principles of prompt design with rigorous explanations, good vs. bad examples, and actionable best practices.")

    # Overview banner
    st.markdown(
        """
        <div class="piq-hero">
            <h1 style="font-size: 1.35rem;">Architectural Prompt Engineering Principles</h1>
            <p style="font-size: 0.95rem;">
                Modern Large Language Models respond to semantic priming, structural constraints, and cognitive decomposition.
                Review the core techniques below and explore how each transforms model output quality.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for topic in EDUCATIONAL_TOPICS:
        with st.expander(f"📖 {topic['title']}", expanded=(topic["id"] in ["role_prompting", "chain_of_thought"])):
            st.markdown(f"<span class='piq-badge piq-badge-good'>{topic['badge']}</span>", unsafe_allow_html=True)
            
            st.markdown("#### The Concept")
            st.write(topic["concept"])

            st.markdown("#### Why It Matters")
            st.write(topic["why_it_matters"])

            if topic["id"] == "chain_of_thought":
                st.warning(
                    "⚠️ **Chain-of-Thought Guidance:** When prompting for reasoning, explicitly ask the model to produce "
                    "concise reasoning summaries, structured intermediate steps, or verification checklists. Avoid attempting to "
                    "extract or force private internal reasoning streams, as modern models perform best when producing clear, "
                    "auditable rationale steps directly in the visible response."
                )

            st.markdown("#### Comparative Contrast")
            col_poor, col_good = st.columns(2)
            with col_poor:
                st.markdown("**❌ Weak / Naive Prompt**")
                st.markdown(
                    f"""
                    <div style="background-color: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 6px; padding: 0.75rem 1rem; font-family: monospace; font-size: 0.88rem; color: #FCA5A5;">
                        "{topic['poor_example']}"
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_good:
                st.markdown("**✅ Engineered Prompt**")
                st.markdown(
                    f"""
                    <div style="background-color: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.25); border-radius: 6px; padding: 0.75rem 1rem; font-family: monospace; font-size: 0.88rem; color: #86EFAC;">
                        "{topic['good_example']}"
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("#### Best Practices")
            for bp in topic["best_practices"]:
                st.markdown(f"- {bp}")

            # Direct action to test in PromptIQ
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                st.button(
                    f"🔬 Analyze Engineered Prompt",
                    key=f"edu_an_{topic['id']}",
                    on_click=load_prompt_into,
                    args=(topic["good_example"], "🔬 Prompt Analyzer"),
                    use_container_width=True,
                )
            with col_act2:
                st.button(
                    f"⚖️ Compare Weak vs. Engineered in Lab",
                    key=f"edu_cmp_{topic['id']}",
                    on_click=load_prompt_into,
                    args=(topic["poor_example"], "⚖️ Comparison Lab", topic["good_example"]),
                    use_container_width=True,
                )
