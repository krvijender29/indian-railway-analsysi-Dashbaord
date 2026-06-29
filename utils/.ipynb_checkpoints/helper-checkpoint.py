import pandas as pd

def search_train(train_df, train_number):

    result = train_df[
        train_df["properties.number"] == str(train_number)
    ]

    return result

def search_station_code(station_df, code):

    result = station_df[
        station_df["properties.code"] == code.upper()
    ]

    return result

def search_station_name(station_df, name):

    result = station_df[
        station_df["properties.name"].str.contains(
            name,
            case=False,
            na=False
        )
    ]

    return result

def search_schedule(schedule_df, station_code):

    result = schedule_df[
        schedule_df["station_code"] == station_code.upper()
    ]

    return result

def train_route(schedule_df, train_number):

    route = schedule_df[
        schedule_df["train_number"] == str(train_number)
    ]

    return route

def total_trains(train_df):

    return train_df["properties.number"].nunique()

def total_stations(station_df):

    return station_df["properties.code"].nunique()

def total_schedule(schedule_df):

    return len(schedule_df)

def total_zones(station_df):

    return station_df["properties.zone"].nunique()

def busiest_stations(schedule_df):

    return (
        schedule_df["station_code"]
        .value_counts()
        .head(10)
    )