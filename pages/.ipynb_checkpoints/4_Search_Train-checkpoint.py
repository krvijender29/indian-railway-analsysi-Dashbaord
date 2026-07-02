#imports
import streamlit as st

from utils.data_loader import(
    load_train_data,
    load_station_data,
    load_schedule_data
)
#page congig
st.set_page_config(
    page_title="Search",
    page_icon="🔍",
    layout="wide"
)

#loading data
train_df = load_train_data()
station_df = load_station_data()
schedule_df = load_schedule_data()

#Page Title 
st.title(" 🔍 Railway Search")

st.write (
    "Search train,station and schedules."
)

#Adding Search box in Sidebar
search_type = st.sidebar.selectbox(
    "Search By",
    [
        "Train Number",
        "Station Code"
    ]
)

#Search by train number

if search_type == "Train Number":

    train_number = st.text_input(
        "Enter Train Number"
    )

    if train_number:

        result = train_df[train_df["properties.number"] == train_number
        ]

        if result.empty:

            st.error("Wrong Number else this Train is not Data")
        else:

            st.success(
                f"{len(result)} Train Founf"
            )

            st.dataframe(
                result,
                use_container_width = True
            )

#Searching bY Station code
elif search_type == "Station Code":
    station_code = st.text_input(
        "Enter Station Code To Find Loction "
    )
    if station_code:

        result = station_df[station_df["properties.code"]==station_code.upper()]

        if result.empty:

            st.error("Station Not Found in Data")
        else:

            st.success(
                f"{len(result)} Station Found"
            )

            st.dataframe(
                result,
                use_container_width=True
            )
# Train Route Section
st.markdown("---")
st.header("🚆 Train Route")

route_train = st.text_input(
    "Enter train Number to view Route"
)

if route_train:

    route = schedule_df[schedule_df["train_number"] == route_train]

    if route.empty:

        st.error("Train is Not in Data Esle Wrong Train Number")
    else:
        st.success( f"{len(route)} Stops Found")
        st.dataframe(
            route,
            use_container_width=True
        )
# Seach Station Schedule

st.markdown("---")
st.header("📅 Station Schedule")

station_schedule =  st.text_input(
    "Enter Station Code"
)

if station_schedule:

    schedule = schedule_df[

        schedule_df["station_code"] ==
        station_schedule.upper()

    ]

    if schedule.empty:

        st.error("No Records Found")

    else:

        st.success(
            f"{len(schedule)} Records Found"
        )

        st.dataframe(
            schedule,
            use_container_width=True
        )

st.markdown("---")
st.caption(
    "Indian Railway Dashboard | Search"
)
st.markdown("---")

st.warning(
    """
    **Disclaimer:** This dashboard is built for educational and portfolio purposes. 
    The datasets used are sample/publicly available data and may not accurately represent 
    the current Indian Railways network, schedules, routes, or operational information.
    """
)