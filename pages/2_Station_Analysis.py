import streamlit as st
import plotly.express as px

from utils.data_loader import load_station_data

st.set_page_config(
    page_title="Station Analysis",
    page_icon="🚉",
    layout="wide"
)

station_df = load_station_data()

st.title("🚉 Station Analysis Dashboard")

st.markdown(
"""
Analyze Indian Railway Stations based on

- Railway Zone
- State
- Station Search
- Distribution
"""
)

st.sidebar.header("Station Filters")

states = sorted(
    station_df["properties.state"]
    .dropna()
    .unique()
)

selected_state = st.sidebar.selectbox(
    "Select State",
    ["All"] + list(states)
)

zones = sorted(
    station_df["properties.zone"]
    .dropna()
    .unique()
)

selected_zone = st.sidebar.selectbox(
    "Select Railway Zone",
    ["All"] + list(zones)
)



filtered_df = station_df.copy()

if selected_state != "All":
    filtered_df = filtered_df[
        filtered_df["properties.state"] == selected_state
    ]

if selected_zone != "All":
    filtered_df = filtered_df[
        filtered_df["properties.zone"] == selected_zone
    ]

col1, col2, col3, col4 = st.columns(4)
with col1:

    st.metric(
        "Total Stations",
        filtered_df["properties.code"].nunique()
    )

with col2:

    st.metric(
        "States",
        filtered_df["properties.state"].nunique()
    )


with col3:

    st.metric(
        "Zones",
        filtered_df["properties.zone"].nunique()
    )

with col4:

    missing = (
        filtered_df["geometry.coordinates"]
        .isna()
        .sum()
    )

    st.metric(
        "Missing Coordinates",
        missing
    )

st.subheader("🔍 Search Station")

search = st.text_input(
    "Enter Station Name or Code"
)

if search:

    result = filtered_df[
        filtered_df["properties.name"]
        .str.contains(search,
                      case=False,
                      na=False)
        |
        filtered_df["properties.code"]
        .str.contains(search,
                      case=False,
                      na=False)
    ]

else:

    result = filtered_df

st.dataframe(
    result,
    use_container_width=True
)

st.subheader("Stations by State")

state_chart = (
    filtered_df["properties.state"]
    .value_counts()
    .head(10)
    .rename_axis("State")
    .reset_index(name="Stations")
)

fig = px.bar(
    state_chart,
    x="State",
    y="Stations",
    text="Stations",
    title="Top 10 States"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Railway Zones")

zone_chart = (
    filtered_df["properties.zone"]
    .value_counts()
    .rename_axis("Zone")
    .reset_index(name="Stations")
)

fig = px.pie(
    zone_chart,
    values="Stations",
    names="Zone",
    hole=0.4,
    title="Railway Zone Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Top Railway Stations")

st.dataframe(

    filtered_df[
        [
            "properties.code",
            "properties.name",
            "properties.state",
            "properties.zone"
        ]
    ],

    use_container_width=True
)

st.markdown("---")

st.subheader("Dataset Summary")

st.write(f"Total Records : {len(filtered_df)}")

st.markdown("---")

st.caption(
    "Indian Railway Dashboard | Station Analysis"
)


st.warning(
    """
    **Disclaimer:** This dashboard is built for educational and portfolio purposes. 
    The datasets used are sample/publicly available data and may not accurately represent 
    the current Indian Railways network, schedules, routes, or operational information.
    """
)