import streamlit as st

def inject_custom_css():
    """Injects custom CSS for a modern, sleek Indian Railways dashboard theme."""
    st.markdown(
        """
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        /* Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, #0A2F52 0%, #0F4C81 50%, #1B6CA8 100%);
            padding: 2rem 2.2rem;
            border-radius: 16px;
            color: #FFFFFF;
            margin-bottom: 1.8rem;
            box-shadow: 0 10px 25px -5px rgba(10, 47, 82, 0.25);
            border-left: 6px solid #F39C12;
            position: relative;
            overflow: hidden;
        }

        .hero-title {
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin: 0;
            color: #FFFFFF;
        }

        .hero-subtitle {
            font-size: 1.02rem;
            color: #E2E8F0;
            margin-top: 0.5rem;
            max-width: 800px;
            line-height: 1.5;
            font-weight: 400;
        }

        /* KPI Metric Cards */
        .kpi-card {
            background: #FFFFFF;
            border-radius: 14px;
            padding: 1.2rem 1.3rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(226, 232, 240, 0.9);
            transition: all 0.25s ease-in-out;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 120px;
        }

        .kpi-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 24px rgba(15, 76, 129, 0.12);
            border-color: #0F4C81;
        }

        .kpi-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.6rem;
        }

        .kpi-title {
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748B;
        }

        .kpi-icon-box {
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
        }

        .kpi-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: #0F2942;
            letter-spacing: -0.02em;
            line-height: 1.1;
            margin-bottom: 0.3rem;
        }

        .kpi-subtext {
            font-size: 0.78rem;
            color: #0E8388;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }

        /* Nav Cards */
        .nav-card {
            background: #FFFFFF;
            border-radius: 14px;
            padding: 1.4rem;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
            transition: all 0.25s ease;
            height: 100%;
        }

        .nav-card:hover {
            transform: translateY(-4px);
            border-color: #0F4C81;
            box-shadow: 0 10px 20px rgba(15, 76, 129, 0.1);
        }

        .nav-card-icon {
            font-size: 2rem;
            margin-bottom: 0.6rem;
        }

        .nav-card-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0F2942;
            margin-bottom: 0.3rem;
        }

        .nav-card-desc {
            font-size: 0.86rem;
            color: #64748B;
            line-height: 1.45;
        }

        /* Badges */
        .pill-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            margin: 0.15rem;
        }

        .pill-primary { background: #E0F2FE; color: #0369A1; }
        .pill-success { background: #DCFCE7; color: #15803D; }
        .pill-warning { background: #FEF3C7; color: #B45309; }
        .pill-danger  { background: #FEE2E2; color: #B91C1C; }
        .pill-purple  { background: #F3E8FF; color: #7E22CE; }

        /* Custom Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background-color: #F8FAFC;
            padding: 5px;
            border-radius: 10px;
            border: 1px solid #E2E8F0;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            padding: 6px 16px;
            color: #64748B;
        }

        .stTabs [aria-selected="true"] {
            background-color: #0F4C81 !important;
            color: #FFFFFF !important;
            box-shadow: 0 2px 6px rgba(15, 76, 129, 0.25);
        }

        /* Profile Card */
        .profile-card {
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 14px;
            padding: 1.4rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.2rem;
        }

        /* Clean Footer */
        .footer-container {
            margin-top: 2.5rem;
            padding-top: 1.2rem;
            border-top: 1px solid #E2E8F0;
            text-align: center;
            color: #64748B;
            font-size: 0.82rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_hero_banner(title, subtitle, badge="Indian Railways Analytics Hub"):
    """Renders a modern hero banner."""
    st.markdown(
        f"""
        <div class="hero-banner">
            <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #F39C12; margin-bottom: 0.3rem;">
                ★ {badge}
            </div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_kpi_card(title, value, subtext="", icon="🚆", icon_bg="#E0F2FE"):
    """Renders an interactive KPI metric card."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">{title}</span>
                <div class="kpi-icon-box" style="background-color: {icon_bg};">
                    {icon}
                </div>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtext">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_section_header(title, subtitle=""):
    """Renders a clean section header with optional subtitle."""
    sub_html = f"<span style='font-size: 0.85rem; color: #64748B; font-weight: 500;'>{subtitle}</span>" if subtitle else ""
    st.markdown(
        f"""
        <div style="display: flex; align-items: baseline; justify-content: space-between; margin-top: 1.2rem; margin-bottom: 0.8rem; border-bottom: 2px solid #F1F5F9; padding-bottom: 0.4rem;">
            <h3 style="margin: 0; font-weight: 700; color: #0F2942;">{title}</h3>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_disclaimer():
    """Renders a standard educational disclaimer."""
    st.markdown(
        """
        <div class="footer-container">
            <div style="font-weight: 600; color: #475569; margin-bottom: 0.2rem;">
                🚆 Indian Railway Intelligence & Analytics Dashboard
            </div>
            <div style="font-size: 0.76rem; color: #94A3B8; max-width: 700px; margin: 0 auto;">
                Disclaimer: Built for analytical and educational portfolio exploration. Underlying datasets are sample representations of Indian Railways network data.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
