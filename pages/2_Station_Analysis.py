import streamlit as st
import pandas as pd

from utils.ui_components import (
    inject_custom_css,
    render_hero_banner,
    render_kpi_card,
    render_section_header,
    render_disclaimer
)
from utils.data_loader import load_station_data
from utils.helper import (
    total_stations,
    total_zones,
    search_station
)
from utils.charts import (
    plot_station_map,
    plot_state_distribution_bar,
    plot_zone_distribution_pie
)

st.set_page_config(
    page_title="Station Geospatial & Zone Analysis",
    page_icon="🚉",
    layout="wide"
)

inject_custom_css()

# Load Station Data
station_df = load_station_data()

# Hero Header
render_hero_banner(
    title="🚉 Station Geospatial & Network Analysis",
    subtitle="Interactive spatial mapping, state and railway zone distribution across all Indian Railway stations and junctions.",
    badge="Spatial Intelligence"
)

# Sidebar Filters
st.sidebar.markdown("### 🎛️ Station Filters")

all_states = sorted(station_df["properties.state"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    "Filter by State",
    options=all_states,
    default=[]
)

all_zones = sorted(station_df["properties.zone"].dropna().unique().tolist())
selected_zones = st.sidebar.multiselect(
    "Filter by Railway Zone",
    options=all_zones,
    default=[]
)

only_gps = st.sidebar.checkbox("📍 Only stations with GPS coordinates", value=False)

# Apply Filters
filtered_df = station_df.copy()

if selected_states:
    filtered_df = filtered_df[filtered_df["properties.state"].isin(selected_states)]

if selected_zones:
    filtered_df = filtered_df[filtered_df["properties.zone"].isin(selected_zones)]

if only_gps:
    filtered_df = filtered_df.dropna(subset=["latitude", "longitude"])

if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
    st.rerun()

# Dynamic KPI Cards
has_gps_count = filtered_df["latitude"].notna().sum()
missing_gps_count = filtered_df["latitude"].isna().sum()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    render_kpi_card(
        title="Filtered Stations",
        value=f"{len(filtered_df):,}",
        subtext=f"of {len(station_df):,} total stations",
        icon="🚉",
        icon_bg="#E0F2FE"
    )

with kpi2:
    render_kpi_card(
        title="States Covered",
        value=f"{filtered_df['properties.state'].nunique()}",
        subtext="States & UTs",
        icon="🏛️",
        icon_bg="#FEF3C7"
    )

with kpi3:
    render_kpi_card(
        title="Railway Zones",
        value=f"{filtered_df['properties.zone'].nunique()}",
        subtext="Operating zones",
        icon="🗺️",
        icon_bg="#DCFCE7"
    )

with kpi4:
    render_kpi_card(
        title="GPS Mapped",
        value=f"{has_gps_count:,}",
        subtext=f"{(has_gps_count / len(filtered_df) * 100):.1f}% mapped" if len(filtered_df) > 0 else "0%",
        icon="📍",
        icon_bg="#EDE9FE"
    )

with kpi5:
    render_kpi_card(
        title="Missing Coordinates",
        value=f"{missing_gps_count:,}",
        subtext="Without GPS lat/lon",
        icon="⚠️",
        icon_bg="#FEE2E2"
    )

st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)

# Tabs Layout
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Geospatial Map",
    "📊 State & Zone Distribution",
    "🔍 Quick Station Lookup",
    "📋 Station Directory & Export"
])

with tab1:
    render_section_header("Geospatial Station Network Map", "Interactive map of station coordinates across India")
    
    col_map_opt1, col_map_opt2 = st.columns([1, 3])
    with col_map_opt1:
        color_choice = st.selectbox("Color Markers By:", ["Railway Zone", "State"], index=0)
        color_col = "properties.zone" if color_choice == "Railway Zone" else "properties.state"
        
    fig_map = plot_station_map(filtered_df, color_by=color_col, max_points=3500)
    st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    render_section_header("State-Wise & Zone-Wise Station Densities")
    col_chart1, col_chart2 = st.columns([3, 2])
    
    with col_chart1:
        st.plotly_chart(plot_state_distribution_bar(filtered_df, n=15), use_container_width=True)
        
    with col_chart2:
        st.plotly_chart(plot_zone_distribution_pie(filtered_df, title="Station Distribution by Zone"), use_container_width=True)

with tab3:
    render_section_header("Quick Station Search")
    
    search_query = st.text_input("🔍 Enter Station Code (e.g., NDLS, CSMT, HWH) or Station Name", "")
    
    if search_query:
        search_res = search_station(filtered_df, search_query)
        if not search_res.empty:
            st.success(f"Found **{len(search_res)}** matching station(s):")
            
            for _, s_row in search_res.head(5).iterrows():
                s_code = s_row.get("properties.code", "")
                s_name = s_row.get("properties.name", "")
                s_state = s_row.get("properties.state", "")
                s_zone = s_row.get("properties.zone", "")
                s_addr = s_row.get("properties.address", "")
                s_lat = s_row.get("latitude", "N/A")
                s_lon = s_row.get("longitude", "N/A")
                
                st.markdown(
                    f"""
                    <div class="profile-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <div class="profile-title">{s_name} <span class="profile-code">{s_code}</span></div>
                            <div>
                                <span class="pill-badge pill-primary">{s_zone} Zone</span>
                                <span class="pill-badge pill-warning">{s_state}</span>
                            </div>
                        </div>
                        <div style="font-size: 0.9rem; color: #475569; margin-bottom: 0.3rem;">
                            📍 <b>Address:</b> {s_addr if s_addr else 'Not specified'}
                        </div>
                        <div style="font-size: 0.82rem; color: #64748B;">
                            🌐 <b>Coordinates:</b> Lat: {s_lat}, Lon: {s_lon}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning(f"No station found matching '{search_query}' within active filters.")
    else:
        st.info("💡 Type any station code or name above to view its detailed station profile.")

with tab4:
    render_section_header("Station Directory")
    
    cols_to_display = [
        "properties.code", "properties.name", "properties.state", 
        "properties.zone", "properties.address", "latitude", "longitude"
    ]
    cols_present = [c for c in cols_to_display if c in filtered_df.columns]
    
    clean_stations = filtered_df[cols_present].copy()
    clean_stations = clean_stations.rename(columns={
        "properties.code": "Code",
        "properties.name": "Station Name",
        "properties.state": "State",
        "properties.zone": "Zone",
        "properties.address": "Address",
        "latitude": "Latitude",
        "longitude": "Longitude"
    })
    
    st.dataframe(clean_stations, use_container_width=True, height=450, hide_index=True)
    
    st.download_button(
        label="⬇ Download Station Dataset (CSV)",
        data=clean_stations.to_csv(index=False),
        file_name="railway_stations.csv",
        mime="text/csv"
    )

render_disclaimer()