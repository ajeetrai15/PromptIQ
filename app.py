"""PromptIQ — The AI Prompt Engineering Laboratory
Main application entry point.
"""

import os
import streamlit as st

# Initialize page settings must be first Streamlit command
st.set_page_config(
    page_title="PromptIQ — AI Prompt Engineering Laboratory",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.state import init_session_state, sync_navigation
from utils.ui_helpers import inject_custom_styles
from core.gemini_service import get_configured_api_key
from views.analyzer_view import render_analyzer_view
from views.optimizer_view import render_optimizer_view
from views.comparator_view import render_comparator_view
from views.templates_view import render_templates_view
from views.education_view import render_education_view
from views.history_view import render_history_view


def main():
    # Initialize state & custom theme styling
    init_session_state()
    inject_custom_styles()

    # Sidebar
    with st.sidebar:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.8rem;">⚡</span>
                <div>
                    <div style="font-size: 1.25rem; font-weight: 800; letter-spacing: -0.02em; color: #F8FAFC;">PromptIQ</div>
                    <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">Prompt Engineering Lab</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("Evaluate, optimize, and empirically benchmark LLM prompts with Google Gemini.")
        st.markdown("---")

        # API Key Configuration
        st.markdown("##### 🔑 Google Gemini API")
        env_key = get_configured_api_key()
        
        if env_key:
            st.success("API Key detected & active", icon="✅")
            # Allow manual override if desired
            with st.expander("Change or override key"):
                manual_key = st.text_input(
                    "Override Key:",
                    type="password",
                    value=st.session_state.api_key,
                    help="Enter an alternative Gemini API key if desired.",
                )
                if manual_key != st.session_state.api_key:
                    st.session_state.api_key = manual_key
                    st.rerun()
        else:
            st.warning("No API key found in env/secrets", icon="⚠️")
            manual_key = st.text_input(
                "Enter Gemini API Key:",
                type="password",
                value=st.session_state.api_key,
                placeholder="AIzaSy...",
                help="Get a free key from Google AI Studio: https://aistudio.google.com/app/apikey",
            )
            if manual_key != st.session_state.api_key:
                st.session_state.api_key = manual_key
                st.rerun()
            
            st.markdown(
                """
                <div style="font-size: 0.78rem; color: #94A3B8; margin-top: -0.25rem;">
                    💡 <em>Tip: Without an API key, PromptIQ runs in <strong>Demonstration / Offline Mode</strong> so you can explore all features safely.</em>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Model Selector
        st.markdown("##### 🤖 Model Selection")
        model_options = [
            "gemini-3.8-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
        ]
        selected_model = st.selectbox(
            "Select Gemini Model:",
            model_options,
            index=model_options.index(st.session_state.selected_model) if st.session_state.selected_model in model_options else 0,
            help="gemini-3.8-flash is Google's recommended high-speed, structured intelligence model.",
            label_visibility="collapsed",
        )
        st.session_state.selected_model = selected_model

        st.markdown("---")

        # Navigation
        st.markdown("##### 🧭 Navigation")
        nav_options = [
            "🔬 Prompt Analyzer",
            "✨ Prompt Optimizer",
            "⚖️ Comparison Lab",
            "📚 Prompt Templates",
            "🎓 Educational Academy",
            "🕒 History & Vault",
        ]

        # Safely resolve any pending programmatic navigation before widget instantiation
        sync_navigation(nav_options)

        def on_nav_change():
            st.session_state.navigation_page = st.session_state.nav_radio

        current_index = nav_options.index(st.session_state.nav_radio) if st.session_state.nav_radio in nav_options else 0

        selected_page = st.radio(
            "Navigation Menu:",
            nav_options,
            index=current_index,
            key="nav_radio",
            on_change=on_nav_change,
            label_visibility="collapsed",
        )
        st.session_state.navigation_page = selected_page

        st.markdown("---")
        # Sidebar Footer
        st.markdown(
            f"""
            <div style="font-size: 0.75rem; color: #64748B; line-height: 1.4;">
                <strong>PromptIQ v1.0.0</strong><br>
                Official <code>google-genai</code> SDK<br>
                History items: {len(st.session_state.history)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Main Area Banner
    st.markdown(
        """
        <div class="piq-hero">
            <h1>PromptIQ — The AI Prompt Engineering Laboratory</h1>
            <p>Understand, evaluate, improve, and experimentally benchmark AI prompts with structured diagnostics and live dual-inference testing.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Route Page
    page = st.session_state.navigation_page

    if page == "🔬 Prompt Analyzer":
        render_analyzer_view()
    elif page == "✨ Prompt Optimizer":
        render_optimizer_view()
    elif page == "⚖️ Comparison Lab":
        render_comparator_view()
    elif page == "📚 Prompt Templates":
        render_templates_view()
    elif page == "🎓 Educational Academy":
        render_education_view()
    elif page == "🕒 History & Vault":
        render_history_view()


if __name__ == "__main__":
    main()
