import streamlit as st
import plotly.express as px

from utils.data_loader import load_train_data

st.set_page_config(
    page_title="Train Analysis",
    page_icon="🚆",
    layout="wide"
)

train_df = load_train_data()

st.title("🚆 Train Analysis Dashboard")

st.markdown(
"""
Analyze train routes, journey distance,
duration and train categories.
"""
)

st.sidebar.header("Filters")

train_types = sorted(
    train_df["properties.type"].dropna().unique()
)

selected_type = st.sidebar.selectbox(
    "Train Type",
    ["All"] + list(train_types)
)

zones = sorted(
    train_df["properties.zone"].dropna().unique()
)

selected_zone = st.sidebar.selectbox(
    "Railway Zone",
    ["All"] + list(zones)
)

filtered_df = train_df.copy()

if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["properties.type"] == selected_type
    ]

if selected_zone != "All":
    filtered_df = filtered_df[
        filtered_df["properties.zone"] == selected_zone
    ]

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Trains",
        filtered_df["properties.number"].nunique()
    )

with col2:

    st.metric(
        "Average Distance",
        round(
            filtered_df["properties.distance"].mean(),
            2
        )
    )

with col3:

    st.metric(
        "Average Duration",
        round(
            filtered_df["properties.duration_h"].mean(),
            2
        )
    )

with col4:

    st.metric(
        "Zones",
        filtered_df["properties.zone"].nunique()
    )

st.subheader("🚆 Train Type Distribution")

fig = px.bar(
    filtered_df["properties.type"]
    .value_counts()
    .reset_index(),
    x="properties.type",
    y="count",
    labels={
        "properties.type":"Train Type",
        "count":"Count"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Journey Distance")

fig = px.histogram(
    filtered_df,
    x="properties.distance",
    nbins=30,
    title="Distance Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Journey Duration")

fig = px.histogram(
    filtered_df,
    x="properties.duration_h",
    nbins=30,
    title="Duration Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)