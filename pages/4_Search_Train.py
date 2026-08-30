import streamlit as st
import pandas as pd

from utils.ui_components import (
    inject_custom_css,
    render_hero_banner,
    render_section_header,
    render_disclaimer
)
from utils.data_loader import load_all_data
from utils.helper import (
    search_train,
    search_station,
    train_route,
    search_schedule,
    find_direct_trains
)
from utils.charts import plot_single_train_route_map

st.set_page_config(
    page_title="Smart Railway Search & Route Tracker",
    page_icon="🔍",
    layout="wide"
)

inject_custom_css()

# Load All Data
train_df, station_df, schedule_df = load_all_data()

# Hero Header
render_hero_banner(
    title="🔍 Smart Railway Search & Route Tracker",
    subtitle="Search any Indian Railways train, inspect live station timetables, visualize geographic route maps, or find direct trains between two cities.",
    badge="Search Intelligence"
)

# Search Mode Selector
search_mode = st.radio(
    "Select Search Mode:",
    ["🚆 Train Route & Map Tracker", "🚉 Station Live Arrival Board", "🛤️ Direct Train Finder (Source ➔ Destination)"],
    horizontal=True
)

st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

# ----------------------------------------------------
# MODE 1: Train Search & Live Route Timeline & Map
# ----------------------------------------------------
if search_mode == "🚆 Train Route & Map Tracker":
    render_section_header("Train Profile & Route Map Lookup")
    
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        train_query = st.text_input(
            "Enter Train Number (e.g. 12951, 12002, 12301) or Train Name (e.g. Rajdhani, Shatabdi, Express):",
            value="12951",
            placeholder="Type train number or name..."
        )
    
    if train_query:
        matches = search_train(train_df, train_query)
        
        if matches.empty:
            st.warning(f"No train found matching '{train_query}'. Please check the number or name.")
        else:
            if len(matches) > 1:
                st.info(f"Found **{len(matches)}** matching trains. Select one below:")
                train_labels = [
                    f"{row.get('properties.number', '')} - {row.get('properties.name', '')} ({row.get('properties.from_station_name', '')} ➔ {row.get('properties.to_station_name', '')})"
                    for _, row in matches.iterrows()
                ]
                selected_idx = st.selectbox("Select Train:", range(len(train_labels)), format_func=lambda x: train_labels[x])
                selected_train = matches.iloc[selected_idx]
            else:
                selected_train = matches.iloc[0]
                
            # Train Details
            t_num = selected_train.get("properties.number", "")
            t_name = selected_train.get("properties.name", "Unknown")
            t_type = selected_train.get("properties.type", "Express")
            t_zone = selected_train.get("properties.zone", "IR")
            from_name = selected_train.get("properties.from_station_name", "Origin")
            from_code = selected_train.get("properties.from_station_code", "")
            to_name = selected_train.get("properties.to_station_name", "Destination")
            to_code = selected_train.get("properties.to_station_code", "")
            dist = selected_train.get("properties.distance", 0)
            dur = selected_train.get("total_duration_hours", 0)
            speed = selected_train.get("speed_kmh", 0)
            dep_time = selected_train.get("properties.departure", "N/A")
            arr_time = selected_train.get("properties.arrival", "N/A")
            
            # Coach Classes
            classes = []
            if selected_train.get("properties.first_ac") == 1: classes.append("1st AC (1A)")
            if selected_train.get("properties.second_ac") == 1: classes.append("2nd AC (2A)")
            if selected_train.get("properties.third_ac") == 1: classes.append("3rd AC (3A)")
            if selected_train.get("properties.sleeper") == 1: classes.append("Sleeper (SL)")
            if selected_train.get("properties.chair_car") == 1: classes.append("Chair Car (CC)")
            if selected_train.get("properties.first_class") == 1: classes.append("First Class (FC)")
            
            classes_html = " ".join([f"<span class='pill-badge pill-purple'>{c}</span>" for c in classes]) if classes else "<span class='pill-badge pill-warning'>General Unreserved / Standard</span>"
            
            # Render Train Profile Card
            st.markdown(
                f"""
                <div class="profile-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                        <div>
                            <span class="profile-code">{t_num}</span>
                            <span class="profile-title" style="margin-left: 0.5rem;">{t_name}</span>
                        </div>
                        <div>
                            <span class="pill-badge pill-primary">{t_type}</span>
                            <span class="pill-badge pill-success">{t_zone} Zone</span>
                        </div>
                    </div>
                    <div style="font-size: 1.05rem; color: #1E293B; margin-bottom: 0.6rem; font-weight: 600;">
                        🛤️ {from_name} ({from_code}) ➔ {to_name} ({to_code})
                    </div>
                    <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; font-size: 0.88rem; color: #475569; margin-bottom: 0.8rem;">
                        <span>📏 <b>Distance:</b> {dist:,} km</span>
                        <span>⏱️ <b>Duration:</b> {dur} hrs</span>
                        <span>⚡ <b>Avg Speed:</b> {speed} km/h</span>
                        <span>⏰ <b>Departure:</b> {dep_time}</span>
                        <span>🏁 <b>Arrival:</b> {arr_time}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #64748B;">
                        🛋️ <b>Available Classes:</b> {classes_html}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Route Map & Timetable Layout
            map_view, table_view = st.columns([1, 1])
            
            with map_view:
                st.markdown("##### 🗺️ Geographic Route Path")
                fig_route = plot_single_train_route_map(selected_train.to_dict(), station_df=station_df)
                if fig_route:
                    st.plotly_chart(fig_route, use_container_width=True)
                else:
                    st.info("No spatial LineString coordinates available for this specific train route.")
                    
            with table_view:
                st.markdown("##### 📋 Scheduled Halts & Timetable")
                route_schedule = train_route(schedule_df, t_num)
                if not route_schedule.empty:
                    disp_sched = route_schedule[["day", "station_code", "station_name", "arrival", "departure"]].copy()
                    disp_sched.columns = ["Day", "Code", "Station Name", "Arrival", "Departure"]
                    st.dataframe(disp_sched, use_container_width=True, height=450, hide_index=True)
                else:
                    st.info("Detailed halt schedule records not found for this train number.")


# ----------------------------------------------------
# MODE 2: Station Search & Live Station Board
# ----------------------------------------------------
elif search_mode == "🚉 Station Live Arrival Board":
    render_section_header("Station Profile & Live Timetable Board")
    
    st_query = st.text_input(
        "Enter Station Code (e.g. NDLS, CSMT, HWH, BRC, PNBE) or Station Name:",
        value="NDLS",
        placeholder="Type station code or name..."
    )
    
    if st_query:
        st_matches = search_station(station_df, st_query)
        
        if st_matches.empty:
            st.warning(f"No station found matching '{st_query}'.")
        else:
            if len(st_matches) > 1:
                st.info(f"Found **{len(st_matches)}** matching stations. Select one:")
                st_labels = [
                    f"{row.get('properties.code', '')} - {row.get('properties.name', '')} ({row.get('properties.state', '')})"
                    for _, row in st_matches.iterrows()
                ]
                sel_st_idx = st.selectbox("Select Station:", range(len(st_labels)), format_func=lambda x: st_labels[x])
                selected_st = st_matches.iloc[sel_st_idx]
            else:
                selected_st = st_matches.iloc[0]
                
            s_code = selected_st.get("properties.code", "")
            s_name = selected_st.get("properties.name", "")
            s_state = selected_st.get("properties.state", "")
            s_zone = selected_st.get("properties.zone", "")
            s_addr = selected_st.get("properties.address", "")
            s_lat = selected_st.get("latitude", "N/A")
            s_lon = selected_st.get("longitude", "N/A")
            
            # Station Board Halts
            st_schedule = search_schedule(schedule_df, s_code)
            
            st.markdown(
                f"""
                <div class="profile-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <div>
                            <span class="profile-title">{s_name}</span>
                            <span class="profile-code">{s_code}</span>
                        </div>
                        <div>
                            <span class="pill-badge pill-primary">{s_zone} Zone</span>
                            <span class="pill-badge pill-warning">{s_state}</span>
                            <span class="pill-badge pill-success">{len(st_schedule)} Halting Trains</span>
                        </div>
                    </div>
                    <div style="font-size: 0.9rem; color: #475569; margin-bottom: 0.3rem;">
                        📍 <b>Location:</b> {s_addr if s_addr else 'Not specified'}
                    </div>
                    <div style="font-size: 0.82rem; color: #64748B;">
                        🌐 <b>GPS Coordinates:</b> Lat {s_lat}, Lon {s_lon}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if not st_schedule.empty:
                st.markdown(f"##### 🚆 Live Timetable Board at {s_name} ({s_code})")
                board_df = st_schedule[["train_number", "train_name", "day", "arrival", "departure"]].copy()
                board_df.columns = ["Train No", "Train Name", "Day", "Arrival Time", "Departure Time"]
                st.dataframe(board_df, use_container_width=True, height=450, hide_index=True)
            else:
                st.info(f"No active scheduled halts found for station code {s_code}.")


# ----------------------------------------------------
# MODE 3: Direct Train Finder (Source to Destination)
# ----------------------------------------------------
elif search_mode == "🛤️ Direct Train Finder (Source ➔ Destination)":
    render_section_header("Find Direct Trains Between Two Stations")
    st.markdown("Search for direct train connections operating between your origin and destination stations.")
    
    col_src, col_dst = st.columns(2)
    with col_src:
        src_code = st.text_input("Origin Station Code (e.g. NDLS, HWH, BRC):", value="NDLS").strip().upper()
    with col_dst:
        dst_code = st.text_input("Destination Station Code (e.g. BRC, CNB, BSB):", value="BRC").strip().upper()
        
    if st.button("🔍 Find Direct Trains", type="primary", use_container_width=True):
        if not src_code or not dst_code:
            st.warning("Please enter both Origin and Destination station codes.")
        elif src_code == dst_code:
            st.warning("Origin and Destination stations cannot be the same.")
        else:
            with st.spinner("Searching direct train routes..."):
                direct_df = find_direct_trains(schedule_df, train_df, src_code, dst_code)
                
            if direct_df.empty:
                st.error(f"No direct trains found running from **{src_code}** to **{dst_code}** in the current dataset.")
            else:
                st.success(f"🎉 Found **{len(direct_df)}** direct train(s) running from **{src_code}** to **{dst_code}**!")
                
                for _, d_row in direct_df.iterrows():
                    t_num = d_row.get("train_number", "")
                    t_name = d_row.get("properties.name", d_row.get("train_name", "Express"))
                    t_type = d_row.get("properties.type", "Express")
                    t_zone = d_row.get("properties.zone", "IR")
                    dep = d_row.get("departure_from", "N/A")
                    arr = d_row.get("arrival_to", "N/A")
                    day_f = d_row.get("day_from", 1)
                    day_t = d_row.get("day_to", 1)
                    tot_dist = d_row.get("properties.distance", "N/A")
                    
                    st.markdown(
                        f"""
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.1rem 1.3rem; margin-bottom: 0.8rem; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                                <div>
                                    <span class="profile-code">{t_num}</span>
                                    <b style="font-size: 1.1rem; color: #0F2942; margin-left: 0.4rem;">{t_name}</b>
                                </div>
                                <div>
                                    <span class="pill-badge pill-primary">{t_type}</span>
                                    <span class="pill-badge pill-success">{t_zone} Zone</span>
                                </div>
                            </div>
                            <div style="display: flex; gap: 2rem; font-size: 0.92rem; color: #334155; margin-top: 0.5rem;">
                                <div>🛫 <b>Depart {src_code}:</b> {dep} (Day {day_f})</div>
                                <div>🛬 <b>Arrive {dst_code}:</b> {arr} (Day {day_t})</div>
                                <div>📏 <b>Total Route:</b> {tot_dist} km</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

render_disclaimer()