import json
import pandas as pd
import streamlit as st


# -----------------------------
# Load Train Dataset
# -----------------------------
@st.cache_data
def load_train_data():

    with open("Data/trains.json", "r") as file:
        train_data = json.load(file)

    train_df = pd.json_normalize(train_data["features"])

    return train_df


# -----------------------------
# Load Station Dataset
# -----------------------------
@st.cache_data
def load_station_data():

    with open("Data/stations.json", "r") as file:
        station_data = json.load(file)

    station_df = pd.json_normalize(station_data["features"])

    return station_df


# -----------------------------
# Load Schedule Dataset
# -----------------------------
@st.cache_data
def load_schedule_data():

    with open("Data/schedules.json", "r") as file:
        schedule_data = json.load(file)

    schedule_df = pd.DataFrame(schedule_data)

    return schedule_df


# -----------------------------
# Load Everything Together
# -----------------------------
@st.cache_data
def load_all_data():

    train_df = load_train_data()

    station_df = load_station_data()

    schedule_df = load_schedule_data()

    return train_df, station_df, schedule_df