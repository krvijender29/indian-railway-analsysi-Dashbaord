import pandas as pd
import numpy as np


# -----------------------------
# Train Search & Lookup
# -----------------------------
def search_train(train_df, query):
    """Search trains by number or name (partial matching)."""
    if train_df.empty or not query:
        return pd.DataFrame()
    query_str = str(query).strip()
    
    # Exact number match or name match
    result = train_df[
        (train_df["properties.number"].astype(str) == query_str) |
        (train_df["properties.name"].str.contains(query_str, case=False, na=False))
    ]
    return result


# -----------------------------
# Station Search & Lookup
# -----------------------------
def search_station(station_df, query):
    """Search stations by code or name (partial matching)."""
    if station_df.empty or not query:
        return pd.DataFrame()
    query_str = str(query).strip().upper()
    
    result = station_df[
        (station_df["properties.code"] == query_str) |
        (station_df["properties.name"].str.contains(query_str, case=False, na=False))
    ]
    return result


def search_station_code(station_df, code):
    """Search stations by exact code."""
    if station_df.empty or not code:
        return pd.DataFrame()
    return station_df[station_df["properties.code"] == str(code).strip().upper()]


def search_station_name(station_df, name):
    """Search stations by name substring."""
    if station_df.empty or not name:
        return pd.DataFrame()
    return station_df[station_df["properties.name"].str.contains(str(name).strip(), case=False, na=False)]


# -----------------------------
# Route & Schedule Helpers
# -----------------------------
def train_route(schedule_df, train_number):
    """Get the full scheduled route for a train number."""
    if schedule_df.empty or not train_number:
        return pd.DataFrame()
    
    route = schedule_df[schedule_df["train_number"] == str(train_number).strip()].copy()
    if not route.empty and "id" in route.columns:
        route = route.sort_values(by=["day", "id"])
    return route


def search_schedule(schedule_df, station_code):
    """Get all trains passing through a station."""
    if schedule_df.empty or not station_code:
        return pd.DataFrame()
    return schedule_df[schedule_df["station_code"] == str(station_code).strip().upper()]


def find_direct_trains(schedule_df, train_df, origin_code, dest_code):
    """Find all direct trains that stop at origin and subsequently at destination."""
    if schedule_df.empty or not origin_code or not dest_code:
        return pd.DataFrame()
    
    origin = str(origin_code).strip().upper()
    dest = str(dest_code).strip().upper()
    
    # Find trains stopping at origin
    origin_halts = schedule_df[schedule_df["station_code"] == origin][["train_number", "id", "day", "departure"]]
    # Find trains stopping at dest
    dest_halts = schedule_df[schedule_df["station_code"] == dest][["train_number", "id", "day", "arrival"]]
    
    # Merge on train_number
    merged = pd.merge(origin_halts, dest_halts, on="train_number", suffixes=("_from", "_to"))
    
    # Filter where destination halt comes AFTER origin halt (by day or id)
    valid_direct = merged[
        (merged["day_to"] > merged["day_from"]) |
        ((merged["day_to"] == merged["day_from"]) & (merged["id_to"] > merged["id_from"]))
    ]
    
    if valid_direct.empty:
        return pd.DataFrame()
    
    # Join with train metadata
    result = pd.merge(
        valid_direct,
        train_df,
        left_on="train_number",
        right_on="properties.number",
        how="left"
    )
    
    return result


# -----------------------------
# Summary Statistics
# -----------------------------
def total_trains(train_df):
    return train_df["properties.number"].nunique() if not train_df.empty else 0


def total_stations(station_df):
    return station_df["properties.code"].nunique() if not station_df.empty else 0


def total_schedule(schedule_df):
    return len(schedule_df) if not schedule_df.empty else 0


def total_zones(df, col_name="properties.zone"):
    if df.empty or col_name not in df.columns:
        return 0
    return df[col_name].dropna().nunique()


def busiest_stations(schedule_df, n=10):
    """Top N busiest stations by number of halts."""
    if schedule_df.empty:
        return pd.Series(dtype=int)
    return schedule_df["station_code"].value_counts().head(n)


def busiest_trains_by_halts(schedule_df, n=10):
    """Top N trains by number of stops/halts."""
    if schedule_df.empty:
        return pd.Series(dtype=int)
    return schedule_df["train_number"].value_counts().head(n)


def train_types(train_df):
    if train_df.empty:
        return pd.Series(dtype=int)
    return train_df["properties.type"].value_counts()


def longest_train(train_df):
    if train_df.empty:
        return pd.DataFrame()
    return train_df.nlargest(1, "properties.distance")


def shortest_train(train_df):
    if train_df.empty:
        return pd.DataFrame()
    return train_df[train_df["properties.distance"] > 0].nsmallest(1, "properties.distance")


def top_longest_trains(train_df, n=10):
    if train_df.empty:
        return pd.DataFrame()
    return train_df.nlargest(n, "properties.distance")


def top_fastest_trains(train_df, n=10):
    """Top N fastest trains with realistic filters (distance > 100km)."""
    if train_df.empty or "speed_kmh" not in train_df.columns:
        return pd.DataFrame()
    valid = train_df[train_df["properties.distance"] >= 100]
    return valid.nlargest(n, "speed_kmh")


def average_distance(train_df):
    if train_df.empty:
        return 0.0
    return round(float(train_df["properties.distance"].mean()), 1)


def average_duration(train_df):
    if train_df.empty:
        return 0.0
    if "total_duration_hours" in train_df.columns:
        return round(float(train_df["total_duration_hours"].mean()), 1)
    return round(float(train_df["properties.duration_h"].mean()), 1)


def average_speed(train_df):
    if train_df.empty or "speed_kmh" not in train_df.columns:
        return 0.0
    valid = train_df[train_df["speed_kmh"] > 0]
    return round(float(valid["speed_kmh"].mean()), 1) if not valid.empty else 0.0


def get_train_class_breakdown(train_df):
    """Counts how many trains offer 1A, 2A, 3A, SL, CC, etc."""
    if train_df.empty:
        return {}
    
    classes = {
        "1st AC (1A)": (train_df["properties.first_ac"] == 1).sum() if "properties.first_ac" in train_df.columns else 0,
        "2nd AC (2A)": (train_df["properties.second_ac"] == 1).sum() if "properties.second_ac" in train_df.columns else 0,
        "3rd AC (3A)": (train_df["properties.third_ac"] == 1).sum() if "properties.third_ac" in train_df.columns else 0,
        "Sleeper (SL)": (train_df["properties.sleeper"] == 1).sum() if "properties.sleeper" in train_df.columns else 0,
        "Chair Car (CC)": (train_df["properties.chair_car"] == 1).sum() if "properties.chair_car" in train_df.columns else 0,
        "First Class (FC)": (train_df["properties.first_class"] == 1).sum() if "properties.first_class" in train_df.columns else 0,
    }
    return classes
