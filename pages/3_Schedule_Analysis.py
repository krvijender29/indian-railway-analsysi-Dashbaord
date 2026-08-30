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
    total_schedule,
    train_route
)
from utils.charts import (
    plot_busiest_stations_bar,
    plot_busiest_trains_bar,
    plot_time_of_day_bar,
    plot_journey_days_line
)

st.set_page_config(
    page_title="Schedule & Traffic Analytics",
    page_icon="📅",
    layout="wide"
)

inject_custom_css()

# Load Data
train_df, station_df, schedule_df = load_all_data()

# Hero Header
render_hero_banner(
    title="📅 Schedule & Traffic Intelligence",
    subtitle="Analyze nationwide train timetables, junction congestion, peak departure hours, and multi-day journey patterns.",
    badge="Operations & Traffic"
)

# Sidebar Filters
st.sidebar.markdown("### 🎛️ Schedule Filters")

day_options = sorted(schedule_df["day"].dropna().unique().tolist())
selected_days = st.sidebar.multiselect(
    "Filter by Journey Day",
    options=day_options,
    default=[]
)

time_options = [
    "Early Morning (4AM - 8AM)",
    "Morning Rush (8AM - 12PM)",
    "Afternoon (12PM - 5PM)",
    "Evening Rush (5PM - 9PM)",
    "Night / Late Night (9PM - 4AM)"
]
selected_windows = st.sidebar.multiselect(
    "Filter by Departure Window",
    options=time_options,
    default=[]
)

# Filter dataframe
filtered_df = schedule_df.copy()

if selected_days:
    filtered_df = filtered_df[filtered_df["day"].isin(selected_days)]

if selected_windows:
    filtered_df = filtered_df[filtered_df["departure_window"].isin(selected_windows)]

if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
    st.rerun()

# Dynamic KPI Cards
avg_stops_per_train = (
    filtered_df.groupby("train_number").size().mean()
    if not filtered_df.empty else 0.0
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    render_kpi_card(
        title="Schedule Halts",
        value=f"{len(filtered_df):,}",
        subtext="Filtered scheduled halts",
        icon="📅",
        icon_bg="#E0F2FE"
    )

with kpi2:
    render_kpi_card(
        title="Unique Trains",
        value=f"{filtered_df['train_number'].nunique():,}",
        subtext="Active trains in selection",
        icon="🚆",
        icon_bg="#FEF3C7"
    )

with kpi3:
    render_kpi_card(
        title="Stations Served",
        value=f"{filtered_df['station_code'].nunique():,}",
        subtext="Active stations in selection",
        icon="🚉",
        icon_bg="#DCFCE7"
    )

with kpi4:
    render_kpi_card(
        title="Avg Halts / Train",
        value=f"{avg_stops_per_train:.1f}",
        subtext="Mean stops per route",
        icon="🛑",
        icon_bg="#EDE9FE"
    )

st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)

# Tabs Layout
tab1, tab2, tab3, tab4 = st.tabs([
    "🚉 Junction Congestion",
    "⏰ Time & Day Patterns",
    "🚆 Timetable Inspector",
    "📋 Schedule Explorer"
])

with tab1:
    render_section_header("Network Congestion & Major Halts")
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            plot_busiest_stations_bar(filtered_df, station_df=station_df, n=15),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            plot_busiest_trains_bar(filtered_df, train_df=train_df, n=10),
            use_container_width=True
        )

with tab2:
    render_section_header("Traffic Dynamics: Peak Hours & Journey Spans")
    col3, col4 = st.columns(2)
    
    with col3:
        st.plotly_chart(
            plot_time_of_day_bar(filtered_df),
            use_container_width=True
        )
    with col4:
        st.plotly_chart(
            plot_journey_days_line(filtered_df),
            use_container_width=True
        )

with tab3:
    render_section_header("Train Timetable & Halt Sequence Inspector")
    
    # Train Selector
    train_opts = sorted(schedule_df["train_number"].unique().tolist())
    
    selected_t = st.selectbox(
        "Select Train Number to view scheduled timetable:",
        options=train_opts[:300],
        help="Type or select a train number"
    )
    
    if selected_t:
        t_route = train_route(schedule_df, selected_t)
        
        # Train Name Lookup
        t_info = train_df[train_df["properties.number"] == str(selected_t)]
        t_name = t_info["properties.name"].iloc[0] if not t_info.empty else "Indian Railway Train"
        t_type = t_info["properties.type"].iloc[0] if not t_info.empty else "Express"
        
        st.markdown(
            f"""
            <div class="profile-card">
                <div style="font-size: 1.3rem; font-weight: 800; color: #0F2942; margin-bottom: 0.3rem;">
                    🚆 {selected_t} - {t_name}
                </div>
                <div style="font-size: 0.88rem; color: #64748B;">
                    <span class="pill-badge pill-primary">{t_type}</span>
                    <span class="pill-badge pill-success">{len(t_route)} Scheduled Stops</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if not t_route.empty:
            display_route = t_route[["day", "station_code", "station_name", "arrival", "departure"]].copy()
            display_route.columns = ["Day", "Station Code", "Station Name", "Arrival Time", "Departure Time"]
            st.dataframe(display_route, use_container_width=True, hide_index=True)

with tab4:
    render_section_header("Explore Schedule Records")
    
    clean_schedule = filtered_df[["train_number", "train_name", "station_code", "station_name", "day", "arrival", "departure"]].copy()
    clean_schedule.columns = ["Train No", "Train Name", "Station Code", "Station Name", "Day", "Arrival", "Departure"]
    
    st.dataframe(clean_schedule, use_container_width=True, height=450, hide_index=True)
    
    st.download_button(
        label="⬇ Download Filtered Schedules (CSV)",
        data=clean_schedule.to_csv(index=False),
        file_name="train_schedules.csv",
        mime="text/csv"
    )

render_disclaimer()