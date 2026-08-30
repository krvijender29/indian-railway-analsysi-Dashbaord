import json
import pandas as pd
import numpy as np
import streamlit as st


# -----------------------------
# Load Train Dataset
# -----------------------------
@st.cache_data(show_spinner=False)
def load_train_data():
    try:
        with open("Data/trains.json", "r", encoding="utf-8") as file:
            train_data = json.load(file)

        train_df = pd.json_normalize(train_data["features"])
        
        # Ensure proper string types for identifiers
        train_df["properties.number"] = train_df["properties.number"].astype(str).str.strip()
        train_df["properties.name"] = train_df["properties.name"].fillna("Unknown Train").astype(str)
        
        # Numeric conversions
        train_df["properties.distance"] = pd.to_numeric(train_df["properties.distance"], errors="coerce").fillna(0)
        train_df["properties.duration_h"] = pd.to_numeric(train_df["properties.duration_h"], errors="coerce").fillna(0)
        train_df["properties.duration_m"] = pd.to_numeric(train_df["properties.duration_m"], errors="coerce").fillna(0)
        
        # Total duration in hours
        total_duration = train_df["properties.duration_h"] + (train_df["properties.duration_m"] / 60.0)
        train_df["total_duration_hours"] = total_duration.round(2)
        
        # Calculate Average Speed (km/h)
        # Avoid division by zero or nonsensical speeds
        speed = np.where(
            (total_duration > 0) & (train_df["properties.distance"] > 0),
            (train_df["properties.distance"] / total_duration).round(1),
            0.0
        )
        # Cap speed outliers at 160 km/h (Vande Bharat / Gatimaan realistic maximums)
        train_df["speed_kmh"] = np.clip(speed, 0, 160)
        
        # Fill missing categories
        train_df["properties.type"] = train_df["properties.type"].fillna("Express").replace("", "Express")
        train_df["properties.zone"] = train_df["properties.zone"].fillna("Unknown").replace("", "Unknown")
        
        return train_df
    except Exception as e:
        st.error(f"Error loading train data: {e}")
        return pd.DataFrame()


# -----------------------------
# Load Station Dataset
# -----------------------------
@st.cache_data(show_spinner=False)
def load_station_data():
    try:
        with open("Data/stations.json", "r", encoding="utf-8") as file:
            station_data = json.load(file)

        station_df = pd.json_normalize(station_data["features"])
        
        station_df["properties.code"] = station_df["properties.code"].astype(str).str.upper().str.strip()
        station_df["properties.name"] = station_df["properties.name"].fillna("Unknown Station").astype(str)
        station_df["properties.state"] = station_df["properties.state"].fillna("Unknown").replace("", "Unknown")
        station_df["properties.zone"] = station_df["properties.zone"].fillna("Unknown").replace("", "Unknown")
        
        # Extract Latitude & Longitude if geometry exists
        def extract_coords(coords):
            if isinstance(coords, (list, tuple)) and len(coords) >= 2:
                lng, lat = coords[0], coords[1]
                if lat is not None and lng is not None and -90 <= lat <= 90 and -180 <= lng <= 180:
                    return pd.Series([lat, lng])
            return pd.Series([np.nan, np.nan])

        if "geometry.coordinates" in station_df.columns:
            coords = station_df["geometry.coordinates"].apply(extract_coords)
            station_df["latitude"] = coords[0]
            station_df["longitude"] = coords[1]
        else:
            station_df["latitude"] = np.nan
            station_df["longitude"] = np.nan
            
        return station_df
    except Exception as e:
        st.error(f"Error loading station data: {e}")
        return pd.DataFrame()


# -----------------------------
# Load Schedule Dataset
# -----------------------------
@st.cache_data(show_spinner=False)
def load_schedule_data():
    try:
        with open("Data/schedules.json", "r", encoding="utf-8") as file:
            schedule_data = json.load(file)

        schedule_df = pd.DataFrame(schedule_data)
        
        schedule_df["train_number"] = schedule_df["train_number"].astype(str).str.strip()
        schedule_df["station_code"] = schedule_df["station_code"].astype(str).str.upper().str.strip()
        schedule_df["station_name"] = schedule_df["station_name"].fillna("Unknown").astype(str)
        schedule_df["day"] = pd.to_numeric(schedule_df["day"], errors="coerce").fillna(1).astype(int)
        
        # Categorize departure time of day (Hour 0-23)
        def get_time_category(time_str):
            if not isinstance(time_str, str) or time_str.lower() == "none" or ":" not in time_str:
                return "Unknown"
            try:
                hour = int(time_str.split(":")[0])
                if 4 <= hour < 8:
                    return "Early Morning (4AM - 8AM)"
                elif 8 <= hour < 12:
                    return "Morning Rush (8AM - 12PM)"
                elif 12 <= hour < 17:
                    return "Afternoon (12PM - 5PM)"
                elif 17 <= hour < 21:
                    return "Evening Rush (5PM - 9PM)"
                else:
                    return "Night / Late Night (9PM - 4AM)"
            except:
                return "Unknown"

        schedule_df["departure_window"] = schedule_df["departure"].apply(get_time_category)
        schedule_df["arrival_window"] = schedule_df["arrival"].apply(get_time_category)
        
        return schedule_df
    except Exception as e:
        st.error(f"Error loading schedule data: {e}")
        return pd.DataFrame()


# -----------------------------
# Load Everything Together
# -----------------------------
@st.cache_data(show_spinner=False)
def load_all_data():
    train_df = load_train_data()
    station_df = load_station_data()
    schedule_df = load_schedule_data()
    return train_df, station_df, schedule_df