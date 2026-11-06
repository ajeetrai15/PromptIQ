"""UI styling, visual helper functions, and custom card components."""

import streamlit as st


def inject_custom_styles():
    """Inject clean, modern CSS suitable for dark and light Streamlit themes."""
    st.markdown(
        """
        <style>
        /* General Layout Tweaks */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        /* Hero Banner */
        .piq-hero {
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.12), rgba(147, 51, 234, 0.08));
            border: 1px solid rgba(79, 70, 229, 0.25);
            border-radius: 12px;
            padding: 1.5rem 1.75rem;
            margin-bottom: 2rem;
        }
        .piq-hero h1 {
            font-size: 1.9rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
            letter-spacing: -0.02em;
        }
        .piq-hero p {
            font-size: 1.05rem;
            color: #94A3B8;
            margin-bottom: 0;
        }

        /* Metric Cards */
        .piq-metric-card {
            background-color: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 1.1rem;
            text-align: left;
            margin-bottom: 0.8rem;
            transition: border-color 0.15s ease;
        }
        .piq-metric-card:hover {
            border-color: rgba(99, 102, 241, 0.4);
        }
        .piq-metric-title {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94A3B8;
            margin-bottom: 0.35rem;
            font-weight: 600;
        }
        .piq-metric-val {
            font-size: 1.75rem;
            font-weight: 700;
            line-height: 1.1;
        }
        .piq-metric-desc {
            font-size: 0.82rem;
            color: #64748B;
            margin-top: 0.4rem;
        }

        /* Badges */
        .piq-badge {
            display: inline-block;
            padding: 0.25rem 0.65rem;
            font-size: 0.75rem;
            font-weight: 600;
            border-radius: 9999px;
            margin-right: 0.4rem;
        }
        .piq-badge-good {
            background-color: rgba(34, 197, 94, 0.15);
            color: #4ADE80;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        .piq-badge-warning {
            background-color: rgba(234, 179, 8, 0.15);
            color: #FACC15;
            border: 1px solid rgba(234, 179, 8, 0.3);
        }
        .piq-badge-poor {
            background-color: rgba(239, 68, 68, 0.15);
            color: #F87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        .piq-badge-neutral {
            background-color: rgba(148, 163, 184, 0.15);
            color: #CBD5E1;
            border: 1px solid rgba(148, 163, 184, 0.25);
        }

        /* Callout Boxes */
        .piq-callout {
            background-color: rgba(30, 41, 59, 0.5);
            border-left: 4px solid #6366F1;
            border-radius: 4px 8px 8px 4px;
            padding: 1rem 1.25rem;
            margin: 1rem 0;
        }

        /* Weakness Card */
        .piq-weakness-card {
            background-color: rgba(239, 68, 68, 0.05);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 8px;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.8rem;
        }
        .piq-weakness-title {
            color: #F87171;
            font-weight: 600;
            font-size: 0.95rem;
            margin-bottom: 0.3rem;
        }
        .piq-weakness-impact {
            color: #CBD5E1;
            font-size: 0.88rem;
            line-height: 1.45;
        }

        /* Empty State */
        .piq-empty-state {
            text-align: center;
            padding: 3rem 1.5rem;
            border: 2px dashed rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            margin: 1.5rem 0;
            color: #94A3B8;
        }
        .piq-empty-state h3 {
            color: #E2E8F0;
            margin-bottom: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_score_badge(score: int) -> str:
    """Return an HTML badge formatted according to the score."""
    if score >= 80:
        cls = "piq-badge-good"
        label = "Strong"
    elif score >= 60:
        cls = "piq-badge-warning"
        label = "Moderate"
    else:
        cls = "piq-badge-poor"
        label = "Needs Work"
    return f'<span class="piq-badge {cls}">{score}/100 • {label}</span>'


def render_metric_card(title: str, score: int, rationale: str):
    """Render a clean metric card with title, score badge, and rationale."""
    badge = render_score_badge(score)
    st.markdown(
        f"""
        <div class="piq-metric-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                <span class="piq-metric-title">{title}</span>
                {badge}
            </div>
            <div class="piq-metric-desc">{rationale}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(title: str, message: str, button_label: str = None) -> bool:
    """Render an informative empty state card."""
    st.markdown(
        f"""
        <div class="piq-empty-state">
            <h3>{title}</h3>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if button_label:
        return st.button(button_label, key=f"empty_btn_{title}")
    return False
