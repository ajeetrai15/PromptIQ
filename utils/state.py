"""Session state and history management for PromptIQ."""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import streamlit as st


def init_session_state() -> None:
    """Initialize all Streamlit session state variables with defaults."""
    if "history" not in st.session_state:
        st.session_state.history = []

    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = ""

    if "optimized_prompt" not in st.session_state:
        st.session_state.optimized_prompt = ""

    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None

    if "optimization_result" not in st.session_state:
        st.session_state.optimization_result = None

    if "comparison_result" not in st.session_state:
        st.session_state.comparison_result = None

    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "gemini-3.8-flash"

    if "navigation_page" not in st.session_state:
        st.session_state.navigation_page = "🔬 Prompt Analyzer"


def add_to_history(
    prompt: str,
    action_type: str,
    details: Optional[Dict[str, Any]] = None,
) -> None:
    """Add a prompt and its metadata to the session history."""
    if not prompt or not prompt.strip():
        return

    # Don't add duplicate if identical to last item
    if st.session_state.history:
        last = st.session_state.history[0]
        if last.get("prompt") == prompt and last.get("action_type") == action_type:
            return

    entry = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prompt": prompt.strip(),
        "action_type": action_type,
        "details": details or {},
    }

    # Prepend newest first, limit to 50
    st.session_state.history.insert(0, entry)
    if len(st.session_state.history) > 50:
        st.session_state.history = st.session_state.history[:50]


def clear_history() -> None:
    """Clear prompt history in session state."""
    st.session_state.history = []


def load_prompt_into(prompt_text: str, target_page: str, optimized_text: str = "") -> None:
    """Helper to navigate to a target page with a prefilled prompt."""
    st.session_state.current_prompt = prompt_text
    if optimized_text:
        st.session_state.optimized_prompt = optimized_text
    st.session_state.navigation_page = target_page
    st.session_state.nav_radio = target_page
