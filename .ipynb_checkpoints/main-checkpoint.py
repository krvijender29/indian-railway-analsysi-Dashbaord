import streamlit as st

from utils.helper import (
    total_trains,
    total_stations,
    total_schedule,
    total_zones
)

from utils.data_loader import load_all_data
train_df, station_df, schedule_df = load_all_data()

st.set_page_config(
    page_title="Indian Railway Analysis Dashboard",
    page_icon="🚆",
    layout="wide"
)

st.title("🚆 Indian Railway Analysis Dashboard")

st.markdown("""
Analyze Indian Railway datasets including

- 🚆 Trains
- 🚉 Stations
- 📅 Train Schedule

using interactive visualizations.
""")

st.sidebar.title("Navigation")

st.sidebar.success("Select a page from the sidebar.")

st.header("Project Overview")

st.write("""
This dashboard provides analytical insights into the Indian Railway network.

The dashboard is divided into four sections:

• Train Analysis

• Station Analysis

• Schedule Analysis

• Search System
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🚆 Total Trains", total_trains(train_df))

with col2:
    st.metric("🚉 Total Stations", total_stations(station_df))

with col3:
    st.metric("📅 Schedule Records", total_schedule(schedule_df))

with col4:
    st.metric("🗺 Railway Zones", total_zones(station_df))

st.subheader("Dashboard Features")

st.markdown("""

✅ Train Analytics

✅ Station Analytics

✅ Schedule Analytics

✅ Interactive Charts

✅ Search by Station Code

✅ Search by Train Number

✅ Data Insights

""")

st.markdown("---")

st.caption("Created by Vijender | Data Analyst Portfolio Project")
