# 🚆 Indian Railway Analysis Dashboard

An interactive **Streamlit** dashboard built using **Python, Pandas, and Plotly** to analyze Indian Railway datasets. The dashboard provides insights into trains, stations, and schedules through interactive visualizations, KPI cards, filters, and search functionality.

🔗 **Live Demo:** [Click here to view the live app](https://tuttm93plpeaiajgsmo6bq.streamlit.app/)

---

## ✨ Features

* 📊 **Dashboard Overview** with KPI Cards
* 🚆 **Train Analysis**

  * Train Type Distribution
  * Journey Distance Analysis
  * Journey Duration Analysis
  * Railway Zone Filter
* 🚉 **Station Analysis**

  * State-wise Station Distribution
  * Zone-wise Station Distribution
  * Station Search
* 📅 **Schedule Analysis**

  * Busiest Stations
  * Train Stop Analysis
  * Journey Day Distribution
  * Download Filtered Data
* 🔍 **Search**

  * Search by Train Number
  * Search by Station Code
  * Search by Station Name
  * View Train Route
  * View Station Schedule

---

## 🗂️ Project Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── trains.json
│   ├── stations.json
│   └── schedules.json
│
├── pages/
│   ├── 1_Train_Analysis.py
│   ├── 2_Station_Analysis.py
│   ├── 3_Schedule_Analysis.py
│   └── 4_Search.py
│
└── utils/
    ├── data_loader.py
    └── helper.py
```

---

## 📊 Dataset

This project uses three JSON datasets:

| Dataset          | Description                                                                     |
| ---------------- | ------------------------------------------------------------------------------- |
| `trains.json`    | Train details including source, destination, distance, duration, and train type |
| `stations.json`  | Station information including station code, name, state, and railway zone       |
| `schedules.json` | Train schedule containing arrival, departure, station code, and train number    |

---

## 🚀 Deployment

This application can be deployed on **Streamlit Community Cloud**.

1. Push the project to a GitHub repository.
2. Open Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select `app.py` as the main file.
5. Deploy the application.

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* Plotly

---

## ⚠️ Disclaimer

This project is developed for **educational, learning, and portfolio purposes only**.

The datasets used are publicly available/sample datasets and may not accurately represent the current Indian Railways network. Train schedules, station information, routes, distances, and other details may differ from official Indian Railways data.

This project is **not affiliated with or endorsed by Indian Railways**.

---

## 🙋 Author

**Vijender**

Engineering Student | Aspiring Data Analyst

If you found this project useful, consider giving it a ⭐ on GitHub.
