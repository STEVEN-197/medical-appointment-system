import streamlit as st

def inject_global_css():
    css = """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #111827 0, #020617 40%, #000000 100%);
        color: #E5E7EB;
        font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(18px);
        border-right: 1px solid rgba(148, 163, 184, 0.35);
    }
    .glass-card {
        background: rgba(15, 23, 42, 0.72);
        border-radius: 22px;
        border: 1px solid rgba(148, 163, 184, 0.45);
        box-shadow: 0 22px 60px rgba(15, 23, 42, 0.90);
        backdrop-filter: blur(24px);
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
    }
    .glass-card-header {
        font-weight: 610;
        font-size: 1rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: #9CA3AF;
        margin-bottom: 0.4rem;
    }
    .primary-text {
        font-weight: 520;
        font-size: 1.25rem;
        color: #E5E7EB;
    }
    .accent-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.12rem 0.65rem;
        border-radius: 999px;
        background: rgba(56, 189, 248, 0.12);
        color: #7DD3FC;
        font-size: 0.74rem;
        border: 1px solid rgba(56, 189, 248, 0.4);
    }
    .stButton>button {
        border-radius: 999px;
        border: 0;
        padding: 0.50rem 1.3rem;
        font-weight: 520;
        background: linear-gradient(135deg, #38BDF8, #22C55E);
        color: #020617;
        box-shadow: 0 12px 30px rgba(56, 189, 248, 0.35);
        transition: all 0.18s ease-out;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 18px 45px rgba(56, 189, 248, 0.55);
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div>div {
        background: rgba(15, 23, 42, 0.95);
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.6);
        color: #F9FAFB;
    }
    .section-title {
        font-size: 1.6rem;
        font-weight: 620;
        margin: 0.2rem 0 1.3rem 0;
        letter-spacing: 0.02em;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

class glass_card:
    def __init__(self, header: str | None = None):
        self.header = header
    def __enter__(self):
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if self.header:
            st.markdown(f'<div class="glass-card-header">{self.header}</div>', unsafe_allow_html=True)
        return self
    def __exit__(self, exc_type, exc, tb):
        st.markdown("</div>", unsafe_allow_html=True)
