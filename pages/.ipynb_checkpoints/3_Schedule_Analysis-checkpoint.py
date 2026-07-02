import streamlit as st
import plotly.express as px

from utils.data_loader import load_schedule_data

st.set_page_config(
    page_title="Schedule Analysis",
    page_icon="📅",
    layout="wide"
)

schedule_df = load_schedule_data()

st.title("📅 Schedule Analysis Dashboard")

st.markdown("""
Analyze train schedules across the Indian Railway network.

Use filters to explore trains, stations and schedule records.
""")

st.sidebar.header("Filters")

train_numbers = sorted(schedule_df["train_number"].unique())

selected_train = st.sidebar.selectbox(
    "Train Number",
    ["All"] + list(train_numbers)
)

station_codes = sorted(schedule_df["station_code"].unique())

selected_station = st.sidebar.selectbox(
    "Station Code",
    ["All"] + list(station_codes)
)

filtered_df = schedule_df.copy()

if selected_train != "All":
    filtered_df = filtered_df[
        filtered_df["train_number"] == selected_train
    ]

if selected_station != "All":
    filtered_df = filtered_df[
        filtered_df["station_code"] == selected_station
    ]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Schedule Records",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Unique Trains",
        filtered_df["train_number"].nunique()
    )

with col3:
    st.metric(
        "Stations",
        filtered_df["station_code"].nunique()
    )

with col4:

    avg = (
        filtered_df
        .groupby("train_number")
        .size()
        .mean()
    )

    st.metric(
        "Avg Stops / Train",
        round(avg,1)
    )

st.subheader("🚉 Top 10 Busiest Stations")

station_chart = (
    filtered_df["station_code"]
    .value_counts()
    .head(10)
    .rename_axis("Station Code")
    .reset_index(name="Train Stops")
)

fig = px.bar(
    station_chart,
    x="Station Code",
    y="Train Stops",
    text="Train Stops",
    color="Train Stops",
    title="Top 10 Busiest Stations"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("🚆 Top 10 Trains by Number of Stops")

train_chart = (
    filtered_df["train_number"]
    .value_counts()
    .head(10)
    .rename_axis("Train Number")
    .reset_index(name="Stops")
)

fig = px.bar(
    train_chart,
    x="Train Number",
    y="Stops",
    text="Stops",
    color="Stops",
    title="Top 10 Trains with Maximum Stops"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("📆 Journey Day Distribution")

day_chart = (
    filtered_df["day"]
    .dropna()
    .value_counts()
    .sort_index()
    .rename_axis("Journey Day")
    .reset_index(name="Records")
)

fig = px.line(
    day_chart,
    x="Journey Day",
    y="Records",
    markers=True,
    title="Schedule Records by Journey Day"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("📋 Schedule Records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)

st.download_button(
    label="⬇ Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_schedule.csv",
    mime="text/csv"
)

st.markdown("---")

st.write(f"Showing **{len(filtered_df)}** schedule records.")

st.markdown("---")

st.caption("Indian Railway Dashboard | Schedule Analysis")


st.warning(
    """
    **Disclaimer:** This dashboard is built for educational and portfolio purposes. 
    The datasets used are sample/publicly available data and may not accurately represent 
    the current Indian Railways network, schedules, routes, or operational information.
    """
)