import streamlit as st
import pandas as pd

from utils.ui_components import (
    inject_custom_css,
    render_hero_banner,
    render_kpi_card,
    render_section_header,
    render_disclaimer
)
from utils.data_loader import load_all_data
from utils.helper import (
    total_trains,
    total_stations,
    total_schedule,
    total_zones,
    average_distance,
    average_speed,
    top_longest_trains
)
from utils.charts import plot_station_map

# Page Configuration
st.set_page_config(
    page_title="Indian Railway Analytics Dashboard",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Modern Design System
inject_custom_css()

# Load Datasets
with st.spinner("Loading railway datasets..."):
    train_df, station_df, schedule_df = load_all_data()

# Hero Banner
render_hero_banner(
    title="🚆 Indian Railway Intelligence & Analytics Hub",
    subtitle="Comprehensive exploratory analysis and interactive spatial intelligence across Indian Railways trains, stations, routes, and schedules.",
    badge="Indian Railways Open Data Explorer"
)

# Sidebar Info
st.sidebar.markdown("### 🚆 Navigation Hub")
st.sidebar.info("Select any page from the sidebar menu above to explore in-depth analytics.")
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Dataset Snapshot:**
    - 🚆 Trains: **{:,}**
    - 🚉 Stations: **{:,}**
    - 📅 Halts: **{:,}**
    """.format(
        total_trains(train_df),
        total_stations(station_df),
        total_schedule(schedule_df)
    )
)

# Executive KPI Grid (6 Cards)
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    render_kpi_card(
        title="Total Trains",
        value=f"{total_trains(train_df):,}",
        subtext="Active fleet & specials",
        icon="🚆",
        icon_bg="#E0F2FE"
    )

with kpi2:
    render_kpi_card(
        title="Stations",
        value=f"{total_stations(station_df):,}",
        subtext="Terminals & halts",
        icon="🚉",
        icon_bg="#FEF3C7"
    )

with kpi3:
    render_kpi_card(
        title="Schedule Records",
        value=f"{total_schedule(schedule_df):,}",
        subtext="Network halt points",
        icon="📅",
        icon_bg="#DCFCE7"
    )

with kpi4:
    render_kpi_card(
        title="Railway Zones",
        value=f"{total_zones(station_df)}",
        subtext="Operating zones",
        icon="🗺️",
        icon_bg="#F3E8FF"
    )

with kpi5:
    render_kpi_card(
        title="Avg Distance",
        value=f"{average_distance(train_df)} km",
        subtext="Mean route length",
        icon="📏",
        icon_bg="#FCE7F3"
    )

with kpi6:
    render_kpi_card(
        title="Avg Speed",
        value=f"{average_speed(train_df)} km/h",
        subtext="Network mean velocity",
        icon="⚡",
        icon_bg="#EDE9FE"
    )

st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

# Feature Navigation Grid
render_section_header("Explore Dashboard Modules", "Deep analytical views categorized by domain")

nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    st.markdown(
        """
        <div class="nav-card">
            <div class="nav-card-icon">🚆</div>
            <div class="nav-card-title">Train Analytics</div>
            <div class="nav-card-desc">
                Analyze fleet categories, speed benchmarks, coach class availability (1A, 2A, 3A, SL, CC), and distance-duration correlations.
            </div>
            <div style="margin-top: 0.8rem;">
                <span class="pill-badge pill-primary">Fleet Overview</span>
                <span class="pill-badge pill-success">Speed Metrics</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with nav2:
    st.markdown(
        """
        <div class="nav-card">
            <div class="nav-card-icon">🚉</div>
            <div class="nav-card-title">Station Analytics</div>
            <div class="nav-card-desc">
                Explore nationwide station distributions, interactive GPS maps across Indian states, and major railway junction hubs.
            </div>
            <div style="margin-top: 0.8rem;">
                <span class="pill-badge pill-primary">Geospatial Map</span>
                <span class="pill-badge pill-warning">State Analysis</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with nav3:
    st.markdown(
        """
        <div class="nav-card">
            <div class="nav-card-icon">📅</div>
            <div class="nav-card-title">Schedule Analytics</div>
            <div class="nav-card-desc">
                Inspect busiest junction halts, peak departure & arrival rush hours, journey day spans, and full train timetable sequences.
            </div>
            <div style="margin-top: 0.8rem;">
                <span class="pill-badge pill-primary">Traffic Peaks</span>
                <span class="pill-badge pill-purple">Halt Sequences</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with nav4:
    st.markdown(
        """
        <div class="nav-card">
            <div class="nav-card-icon">🔍</div>
            <div class="nav-card-title">Smart Search Hub</div>
            <div class="nav-card-desc">
                Search trains by number/name with route timelines, live station arrival boards, and direct source-to-destination train finder.
            </div>
            <div style="margin-top: 0.8rem;">
                <span class="pill-badge pill-danger">Route Map</span>
                <span class="pill-badge pill-success">Direct Finder</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

# Overview Visualizations: Map & Longest Routes
map_col, routes_col = st.columns([3, 2])

with map_col:
    render_section_header("Geospatial Network Coverage", "Preview of station distribution across India")
    fig_map = plot_station_map(station_df, max_points=1200)
    st.plotly_chart(fig_map, use_container_width=True)

with routes_col:
    render_section_header("Network Extremes: Longest Routes", "Top marathon long-distance train journeys")
    longest_df = top_longest_trains(train_df, n=5)
    
    if not longest_df.empty:
        for idx, row in longest_df.iterrows():
            t_num = row.get("properties.number", "N/A")
            t_name = row.get("properties.name", "Unknown")
            dist = row.get("properties.distance", 0)
            dur = row.get("total_duration_hours", 0)
            from_st = row.get("properties.from_station_name", "Origin")
            to_st = row.get("properties.to_station_name", "Destination")
            t_zone = row.get("properties.zone", "IR")
            
            st.markdown(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.9rem 1.1rem; margin-bottom: 0.6rem; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
                        <span style="font-weight: 700; color: #0F2942; font-size: 0.95rem;">{t_num} - {t_name}</span>
                        <span class="pill-badge pill-primary">{t_zone}</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 0.4rem;">
                        🛤️ <b>{from_st}</b> ➔ <b>{to_st}</b>
                    </div>
                    <div style="display: flex; gap: 1rem; font-size: 0.82rem; font-weight: 600; color: #0E8388;">
                        <span>📏 {dist:,} km</span>
                        <span>⏱️ {dur} hrs</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# Disclaimer Footer
render_disclaimer()
