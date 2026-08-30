import streamlit as st
import pandas as pd

from utils.ui_components import (
    inject_custom_css,
    render_hero_banner,
    render_kpi_card,
    render_section_header,
    render_disclaimer
)
from utils.data_loader import load_train_data
from utils.helper import (
    total_trains,
    average_distance,
    average_duration,
    average_speed,
    top_longest_trains,
    top_fastest_trains,
    get_train_class_breakdown
)
from utils.charts import (
    plot_train_types_chart,
    plot_zone_distribution_pie,
    plot_distance_duration_scatter,
    plot_distribution_hist,
    plot_class_availability
)

st.set_page_config(
    page_title="Train Fleet & Performance Analysis",
    page_icon="🚆",
    layout="wide"
)

inject_custom_css()

# Load Train Data
train_df = load_train_data()

# Hero Header
render_hero_banner(
    title="🚆 Train Fleet & Performance Analytics",
    subtitle="Analyze Indian Railways train types, speed metrics, journey distance-duration correlations, and coach classes.",
    badge="Fleet Intelligence"
)

# Sidebar Filters
st.sidebar.markdown("### 🎛️ Train Filters")

all_types = sorted(train_df["properties.type"].dropna().unique().tolist())
selected_types = st.sidebar.multiselect(
    "Filter by Train Type",
    options=all_types,
    default=[]
)

all_zones = sorted(train_df["properties.zone"].dropna().unique().tolist())
selected_zones = st.sidebar.multiselect(
    "Filter by Railway Zone",
    options=all_zones,
    default=[]
)

# Distance Slider
min_dist = int(train_df["properties.distance"].min())
max_dist = int(train_df["properties.distance"].max())
dist_range = st.sidebar.slider(
    "Distance Range (km)",
    min_value=min_dist,
    max_value=max_dist,
    value=(min_dist, max_dist),
    step=50
)

# Filter dataset
filtered_df = train_df.copy()

if selected_types:
    filtered_df = filtered_df[filtered_df["properties.type"].isin(selected_types)]

if selected_zones:
    filtered_df = filtered_df[filtered_df["properties.zone"].isin(selected_zones)]

filtered_df = filtered_df[
    (filtered_df["properties.distance"] >= dist_range[0]) &
    (filtered_df["properties.distance"] <= dist_range[1])
]

# Reset button in sidebar
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.rerun()

# Dynamic KPI Cards
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    render_kpi_card(
        title="Filtered Trains",
        value=f"{len(filtered_df):,}",
        subtext=f"of {len(train_df):,} total trains",
        icon="🚆",
        icon_bg="#E0F2FE"
    )

with kpi2:
    render_kpi_card(
        title="Avg Distance",
        value=f"{average_distance(filtered_df)} km",
        subtext="Filtered mean distance",
        icon="📏",
        icon_bg="#FEF3C7"
    )

with kpi3:
    render_kpi_card(
        title="Avg Duration",
        value=f"{average_duration(filtered_df)} hrs",
        subtext="Filtered mean duration",
        icon="⏱️",
        icon_bg="#DCFCE7"
    )

with kpi4:
    render_kpi_card(
        title="Avg Speed",
        value=f"{average_speed(filtered_df)} km/h",
        subtext="Operating average speed",
        icon="⚡",
        icon_bg="#EDE9FE"
    )

with kpi5:
    render_kpi_card(
        title="Operating Zones",
        value=f"{filtered_df['properties.zone'].nunique()}",
        subtext="Zones covered",
        icon="🗺️",
        icon_bg="#FCE7F3"
    )

st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)

# Tabbed Layout
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Fleet & Categories",
    "⚡ Speed & Correlation",
    "🏆 Extremes & Leaderboards",
    "🛋️ Coach Classes",
    "📋 Data Explorer"
])

with tab1:
    render_section_header("Train Fleet Categorization & Zone Share")
    col_chart1, col_chart2 = st.columns([3, 2])
    
    with col_chart1:
        st.plotly_chart(plot_train_types_chart(filtered_df), use_container_width=True)
        
    with col_chart2:
        st.plotly_chart(plot_zone_distribution_pie(filtered_df, title="Zone Distribution of Filtered Fleet"), use_container_width=True)

with tab2:
    render_section_header("Speed, Distance & Journey Duration Analytics")
    st.plotly_chart(plot_distance_duration_scatter(filtered_df), use_container_width=True)
    
    col_hist1, col_hist2 = st.columns(2)
    with col_hist1:
        st.plotly_chart(
            plot_distribution_hist(
                filtered_df,
                col="properties.distance",
                title="Route Distance Distribution (km)",
                x_label="Distance (km)",
                color="#0F4C81"
            ),
            use_container_width=True
        )
    with col_hist2:
        st.plotly_chart(
            plot_distribution_hist(
                filtered_df,
                col="total_duration_hours",
                title="Journey Duration Distribution (Hours)",
                x_label="Duration (Hours)",
                color="#0E8388"
            ),
            use_container_width=True
        )

with tab3:
    render_section_header("Fleet Records: Longest Routes & Fastest Trains")
    col_long, col_fast = st.columns(2)
    
    with col_long:
        st.markdown("##### 📏 Top 10 Longest Train Routes")
        top_long = top_longest_trains(filtered_df, n=10)
        if not top_long.empty:
            display_long = top_long[[
                "properties.number", "properties.name", "properties.distance", 
                "total_duration_hours", "properties.from_station_name", "properties.to_station_name"
            ]].copy()
            display_long.columns = ["Train No", "Train Name", "Distance (km)", "Duration (hrs)", "Origin", "Destination"]
            st.dataframe(display_long, use_container_width=True, hide_index=True)
        else:
            st.info("No records matching current filters.")
            
    with col_fast:
        st.markdown("##### ⚡ Top 10 Fastest Trains by Average Speed")
        top_fast = top_fastest_trains(filtered_df, n=10)
        if not top_fast.empty:
            display_fast = top_fast[[
                "properties.number", "properties.name", "speed_kmh", 
                "properties.distance", "total_duration_hours", "properties.type"
            ]].copy()
            display_fast.columns = ["Train No", "Train Name", "Avg Speed (km/h)", "Distance (km)", "Duration (hrs)", "Type"]
            st.dataframe(display_fast, use_container_width=True, hide_index=True)
        else:
            st.info("No records matching current filters.")

with tab4:
    render_section_header("Network-wide Coach Class Availability")
    class_breakdown = get_train_class_breakdown(filtered_df)
    st.plotly_chart(plot_class_availability(class_breakdown), use_container_width=True)
    
    st.markdown("##### 💡 Coach Class Summary")
    c_cols = st.columns(6)
    for idx, (cls_name, cnt) in enumerate(class_breakdown.items()):
        with c_cols[idx % 6]:
            pct = (cnt / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            st.metric(label=cls_name, value=f"{cnt:,}", delta=f"{pct:.1f}% of fleet")

with tab5:
    render_section_header("Explore Train Records")
    
    search_q = st.text_input("🔍 Quick Search within filtered records (by name, number, or origin/dest)", "")
    
    table_df = filtered_df.copy()
    if search_q:
        table_df = table_df[
            table_df["properties.name"].str.contains(search_q, case=False, na=False) |
            table_df["properties.number"].str.contains(search_q, case=False, na=False) |
            table_df["properties.from_station_name"].str.contains(search_q, case=False, na=False) |
            table_df["properties.to_station_name"].str.contains(search_q, case=False, na=False)
        ]
        
    cols_to_show = [
        "properties.number", "properties.name", "properties.type", "properties.zone",
        "properties.from_station_name", "properties.to_station_name",
        "properties.distance", "total_duration_hours", "speed_kmh", "properties.departure", "properties.arrival"
    ]
    cols_existing = [c for c in cols_to_show if c in table_df.columns]
    
    cleaned_table = table_df[cols_existing].copy()
    rename_map = {
        "properties.number": "Train No",
        "properties.name": "Train Name",
        "properties.type": "Type",
        "properties.zone": "Zone",
        "properties.from_station_name": "Origin",
        "properties.to_station_name": "Destination",
        "properties.distance": "Distance (km)",
        "total_duration_hours": "Duration (hrs)",
        "speed_kmh": "Avg Speed (km/h)",
        "properties.departure": "Departure",
        "properties.arrival": "Arrival"
    }
    cleaned_table = cleaned_table.rename(columns=rename_map)
    
    st.dataframe(cleaned_table, use_container_width=True, height=450, hide_index=True)
    
    st.download_button(
        label="⬇ Download Filtered Train Dataset (CSV)",
        data=cleaned_table.to_csv(index=False),
        file_name="filtered_trains.csv",
        mime="text/csv",
        use_container_width=False
    )

render_disclaimer()