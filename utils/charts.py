import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Custom color palette inspired by Indian Railways
RAIL_COLORS = [
    "#0F4C81", "#0E8388", "#F39C12", "#C81D25", 
    "#8B5CF6", "#10B981", "#3B82F6", "#EC4899", 
    "#6366F1", "#14B8A6", "#F59E0B", "#EF4444"
]

def _apply_theme(fig, title=""):
    """Applies a clean, modern layout theme to any Plotly figure."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=16, color="#0F2942", family="Plus Jakarta Sans, sans-serif"),
            x=0.01,
            y=0.96
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,250,252,0.6)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#334155", size=12),
        margin=dict(l=20, r=20, t=50 if title else 25, b=25),
        hoverlabel=dict(
            bgcolor="#0F2942",
            font_size=12,
            font_family="Plus Jakarta Sans, sans-serif",
            font_color="#FFFFFF"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#E2E8F0",
            linecolor="#CBD5E1",
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E2E8F0",
            linecolor="#CBD5E1",
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.6)"
        )
    )
    return fig


# -----------------------------
# Train Analytics Charts
# -----------------------------
def plot_train_types_chart(train_df):
    """Horizontal bar chart for train categories with clean counts."""
    if train_df.empty:
        return go.Figure()
    
    counts = train_df["properties.type"].value_counts().reset_index()
    counts.columns = ["Train Type", "Count"]
    
    fig = px.bar(
        counts,
        x="Count",
        y="Train Type",
        orientation="h",
        text="Count",
        color="Count",
        color_continuous_scale="Blues",
        title="Distribution of Train Types"
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Count: %{x:,}<extra></extra>"
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
    return _apply_theme(fig, "🚆 Train Fleet by Category")


def plot_zone_distribution_pie(df, col="properties.zone", title="Railway Zone Distribution"):
    """Donut chart for zone distribution."""
    if df.empty or col not in df.columns:
        return go.Figure()
    
    zone_counts = df[col].value_counts().reset_index()
    zone_counts.columns = ["Zone", "Count"]
    
    fig = px.pie(
        zone_counts,
        names="Zone",
        values="Count",
        hole=0.45,
        color_discrete_sequence=RAIL_COLORS,
        title=title
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>Zone: %{label}</b><br>Total: %{value:,}<br>Share: %{percent}<extra></extra>"
    )
    return _apply_theme(fig, title)


def plot_distance_duration_scatter(train_df):
    """Interactive scatter plot of Distance vs Duration with Speed color scale."""
    if train_df.empty:
        return go.Figure()
    
    # Filter reasonable non-zero records
    sample_df = train_df[(train_df["properties.distance"] > 0) & (train_df["total_duration_hours"] > 0)].copy()
    
    hover_cols = {
        "properties.number": True,
        "properties.name": True,
        "properties.from_station_name": True,
        "properties.to_station_name": True,
        "properties.zone": True,
        "speed_kmh": ":.1f",
        "properties.distance": ":, km",
        "total_duration_hours": ":.1f hrs"
    }
    
    fig = px.scatter(
        sample_df,
        x="properties.distance",
        y="total_duration_hours",
        color="speed_kmh",
        color_continuous_scale="Viridis",
        labels={
            "properties.distance": "Journey Distance (km)",
            "total_duration_hours": "Journey Duration (Hours)",
            "speed_kmh": "Avg Speed (km/h)"
        },
        hover_name="properties.name",
        hover_data=hover_cols,
        title="Distance vs. Duration Correlation & Train Speed"
    )
    fig.update_traces(
        marker=dict(size=7, opacity=0.75, line=dict(width=0.5, color="#FFFFFF"))
    )
    return _apply_theme(fig, "⚡ Distance vs Duration (Color = Avg Speed km/h)")


def plot_distribution_hist(train_df, col="properties.distance", title="Distance Distribution", x_label="Distance (km)", color="#0F4C81", nbins=35):
    """Styled histogram with average indicator."""
    if train_df.empty or col not in train_df.columns:
        return go.Figure()
    
    data = train_df[train_df[col] > 0][col].dropna()
    mean_val = data.mean()
    
    fig = px.histogram(
        train_df[train_df[col] > 0],
        x=col,
        nbins=nbins,
        color_discrete_sequence=[color],
        labels={col: x_label},
        title=title
    )
    fig.add_vline(
        x=mean_val,
        line_dash="dash",
        line_color="#C81D25",
        annotation_text=f"Avg: {mean_val:.1f}",
        annotation_position="top right"
    )
    fig.update_traces(hovertemplate=f"Range: %{{x}}<br>Count: %{{y:,}}<extra></extra>")
    return _apply_theme(fig, title)


def plot_class_availability(class_dict):
    """Horizontal bar chart for coach class breakdown."""
    if not class_dict:
        return go.Figure()
    
    df = pd.DataFrame(list(class_dict.items()), columns=["Class Type", "Trains Offering"])
    df = df.sort_values(by="Trains Offering", ascending=True)
    
    fig = px.bar(
        df,
        x="Trains Offering",
        y="Class Type",
        orientation="h",
        text="Trains Offering",
        color="Trains Offering",
        color_continuous_scale="Teal",
        title="Coach Class Availability Across Network"
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Available on: %{x:,} trains<extra></extra>"
    )
    fig.update_layout(coloraxis_showscale=False)
    return _apply_theme(fig, "🛋️ Coach Class Fleet Availability")


# -----------------------------
# Station Analytics Charts
# -----------------------------
def plot_state_distribution_bar(station_df, n=15):
    """Top states by station count."""
    if station_df.empty:
        return go.Figure()
    
    top_states = station_df["properties.state"].value_counts().head(n).reset_index()
    top_states.columns = ["State", "Station Count"]
    
    fig = px.bar(
        top_states,
        x="State",
        y="Station Count",
        text="Station Count",
        color="Station Count",
        color_continuous_scale="Tealgrn",
        title=f"Top {n} States by Station Count"
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Stations: %{y:,}<extra></extra>"
    )
    fig.update_layout(coloraxis_showscale=False)
    return _apply_theme(fig, f"🏛️ Top {n} States with Most Stations")


def plot_station_map(station_df, color_by="properties.zone", max_points=2500):
    """Geospatial Scattergeo map showing stations across India."""
    if station_df.empty:
        return go.Figure()
    
    # Filter valid coordinates
    valid = station_df.dropna(subset=["latitude", "longitude"]).copy()
    if len(valid) > max_points:
        valid = valid.sample(max_points, random_state=42)
    
    fig = px.scatter_geo(
        valid,
        lat="latitude",
        lon="longitude",
        color=color_by if color_by in valid.columns else None,
        hover_name="properties.name",
        hover_data={
            "properties.code": True,
            "properties.state": True,
            "properties.zone": True,
            "properties.address": True,
            "latitude": False,
            "longitude": False
        },
        color_discrete_sequence=RAIL_COLORS,
        title="Geospatial Station Network Map"
    )
    
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        showcountries=True,
        countrycolor="#94A3B8",
        showland=True,
        landcolor="#F1F5F9",
        showocean=True,
        oceancolor="#E0F2FE",
        showlakes=True,
        lakecolor="#E0F2FE",
        resolution=50
    )
    fig.update_traces(marker=dict(size=4.5, opacity=0.75))
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return _apply_theme(fig, "🗺️ Indian Railway Station Network Map")


# -----------------------------
# Schedule Analytics Charts
# -----------------------------
def plot_busiest_stations_bar(schedule_df, station_df=None, n=15):
    """Top busiest railway stations by number of halts."""
    if schedule_df.empty:
        return go.Figure()
    
    top_stations = schedule_df["station_code"].value_counts().head(n).reset_index()
    top_stations.columns = ["Station Code", "Halts"]
    
    # Merge station name if station_df is provided
    if station_df is not None and not station_df.empty:
        station_names = station_df.drop_duplicates("properties.code").set_index("properties.code")["properties.name"].to_dict()
        top_stations["Station Name"] = top_stations["Station Code"].map(station_names).fillna(top_stations["Station Code"])
        top_stations["Label"] = top_stations["Station Name"] + " (" + top_stations["Station Code"] + ")"
    else:
        top_stations["Label"] = top_stations["Station Code"]
    
    fig = px.bar(
        top_stations,
        x="Halts",
        y="Label",
        orientation="h",
        text="Halts",
        color="Halts",
        color_continuous_scale="Burg",
        title=f"Top {n} Busiest Railway Stations (Halts / Crossings)"
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Total Halts: %{x:,}<extra></extra>"
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
    return _apply_theme(fig, f"🚉 Top {n} Busiest Junctions & Stations")


def plot_busiest_trains_bar(schedule_df, train_df=None, n=10):
    """Top trains with maximum number of stops."""
    if schedule_df.empty:
        return go.Figure()
    
    top_trains = schedule_df["train_number"].value_counts().head(n).reset_index()
    top_trains.columns = ["Train Number", "Stops"]
    
    if train_df is not None and not train_df.empty:
        train_names = train_df.drop_duplicates("properties.number").set_index("properties.number")["properties.name"].to_dict()
        top_trains["Train Name"] = top_trains["Train Number"].map(train_names).fillna(top_trains["Train Number"])
        top_trains["Label"] = top_trains["Train Number"] + " - " + top_trains["Train Name"]
    else:
        top_trains["Label"] = top_trains["Train Number"]
        
    fig = px.bar(
        top_trains,
        x="Stops",
        y="Label",
        orientation="h",
        text="Stops",
        color="Stops",
        color_continuous_scale="Viridis",
        title=f"Top {n} Trains with Maximum Halts"
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Total Halts: %{x:,}<extra></extra>"
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
    return _apply_theme(fig, f"🚆 Top {n} Trains with Most Stops")


def plot_time_of_day_bar(schedule_df):
    """Departure time window distribution."""
    if schedule_df.empty or "departure_window" not in schedule_df.columns:
        return go.Figure()
    
    order = [
        "Early Morning (4AM - 8AM)",
        "Morning Rush (8AM - 12PM)",
        "Afternoon (12PM - 5PM)",
        "Evening Rush (5PM - 9PM)",
        "Night / Late Night (9PM - 4AM)"
    ]
    
    dep_counts = schedule_df["departure_window"].value_counts().reindex(order).fillna(0).reset_index()
    dep_counts.columns = ["Time Window", "Departures"]
    
    fig = px.bar(
        dep_counts,
        x="Time Window",
        y="Departures",
        text="Departures",
        color="Time Window",
        color_discrete_sequence=RAIL_COLORS,
        title="Schedule Traffic by Departure Time of Day"
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Departures: %{y:,}<extra></extra>"
    )
    fig.update_layout(showlegend=False)
    return _apply_theme(fig, "⏰ Departure Time-of-Day Traffic Distribution")


def plot_journey_days_line(schedule_df):
    """Line chart showing schedule records across journey days."""
    if schedule_df.empty or "day" not in schedule_df.columns:
        return go.Figure()
    
    day_counts = schedule_df["day"].value_counts().sort_index().reset_index()
    day_counts.columns = ["Journey Day", "Halts Count"]
    day_counts["Day Label"] = "Day " + day_counts["Journey Day"].astype(str)
    
    fig = px.line(
        day_counts,
        x="Day Label",
        y="Halts Count",
        markers=True,
        title="Journey Day Span Distribution",
        color_discrete_sequence=["#0F4C81"]
    )
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=9, color="#C81D25"),
        hovertemplate="<b>%{x}</b><br>Halts: %{y:,}<extra></extra>"
    )
    return _apply_theme(fig, "📆 Journey Day Span Distribution")


def plot_single_train_route_map(train_feature, station_df=None):
    """Plots a single train's LineString geometry coordinates on an India map."""
    if not train_feature or "geometry.coordinates" not in train_feature:
        return None
    
    coords = train_feature.get("geometry.coordinates", [])
    if not coords or not isinstance(coords, list):
        return None
    
    lons = [c[0] for c in coords if isinstance(c, list) and len(c) >= 2]
    lats = [c[1] for c in coords if isinstance(c, list) and len(c) >= 2]
    
    if not lats or not lons:
        return None
    
    fig = go.Figure()
    
    # Route Line
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        mode="lines+markers",
        line=dict(width=3, color="#C81D25"),
        marker=dict(size=4, color="#0F4C81"),
        name="Route Path",
        hoverinfo="none"
    ))
    
    # Origin & Destination markers
    t_name = train_feature.get("properties.name", "Train")
    t_num = train_feature.get("properties.number", "")
    from_name = train_feature.get("properties.from_station_name", "Origin")
    to_name = train_feature.get("properties.to_station_name", "Destination")
    
    fig.add_trace(go.Scattergeo(
        lon=[lons[0], lons[-1]],
        lat=[lats[0], lats[-1]],
        mode="markers+text",
        marker=dict(size=12, color=["#10B981", "#EF4444"], symbol="circle"),
        text=[f"Origin: {from_name}", f"Dest: {to_name}"],
        textposition=["top center", "bottom center"],
        name="Endpoints",
        hovertemplate="<b>%{text}</b><extra></extra>"
    ))
    
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        showcountries=True,
        countrycolor="#94A3B8",
        showland=True,
        landcolor="#F8FAFC",
        showocean=True,
        oceancolor="#E0F2FE",
        resolution=50
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=35, b=0),
        showlegend=False
    )
    return _apply_theme(fig, f"🗺️ Route Map: {t_num} - {t_name}")
