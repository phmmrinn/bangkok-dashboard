import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Bangkok Traffic & Urban Dashboard", layout="wide")

# -------------------------------------------------
# DATA
# -------------------------------------------------
data = {
    "year": [2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    "vehicles_million": [9.02,9.36,9.77,9.82,10.69,10.97,11.24,11.62,11.98,12.22],
    "speed_kmh": [35.06,33.98,29.04,25.54,24.62,28.40,27.70,26.30,25.33,24.12],
    "green_area": [23.5,22.8,22.1,21.5,20.8,20.0,18.9,18.3,17.7,17.2],
    "population_million": [5.70,5.68,5.67,5.66,5.67,5.48,5.40,5.35,5.30,5.26]
}
df = pd.DataFrame(data)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("🌆 Bangkok Traffic & Urban Dashboard")
st.caption("รถยนต์ • ความเร็ว • พื้นที่สีเขียว • ประชากร (2558–2567)")
st.markdown("---")

# -------------------------------------------------
# FILTERS
# -------------------------------------------------
year_selected = st.sidebar.selectbox("เลือกปีสำหรับ KPI", df["year"], index=len(df)-1)
years_compare = st.sidebar.multiselect(
    "เลือกปีสำหรับกราฟเปรียบเทียบ",
    options=df["year"].tolist(),
    default=[2019, 2020, 2024]
)

# -------------------------------------------------
# KPI SECTION (เลือกปีเดียว)
# -------------------------------------------------
row = df[df["year"] == year_selected].iloc[0]

st.markdown(f"### 📅 ข้อมูลปี {year_selected}")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🚗 รถยนต์จดทะเบียน (ล้านคัน)", f"{row['vehicles_million']:.2f}")
col2.metric("🚦 ความเร็วเฉลี่ย (km/h)", f"{row['speed_kmh']:.2f}")
col3.metric("🌳 พื้นที่สีเขียว (km²)", f"{row['green_area']:.1f}")
col4.metric("👥 ประชากร (ล้านคน)", f"{row['population_million']:.2f}")
st.markdown("---")

# -------------------------------------------------
# LINE CHART (10-YEAR TREND)
# -------------------------------------------------
fig_line = px.line(
    df,
    x="year",
    y=["vehicles_million", "speed_kmh", "green_area", "population_million"],
    markers=True,
    labels={"value":"ค่า (Value)", "variable":"ตัวชี้วัด"},
    title="แนวโน้ม 10 ปี: รถยนต์ / ความเร็ว / พื้นที่สีเขียว / ประชากร",
    color_discrete_map={
        "vehicles_million": "#88B4E7",
        "speed_kmh": "#F7A1A1",
        "green_area": "#93D8A6",
        "population_million": "#C6A8E3"
    }
)
fig_line.update_layout(
    template="simple_white",
    title_x=0.05,
    yaxis_title="ค่า (Value)",
    xaxis_title="ปี (Year)"
)
st.plotly_chart(fig_line, use_container_width=True)
st.markdown("---")

# -------------------------------------------------
# GROUPED BAR CHART (Indicator = group, Year = sub-bar)
# -------------------------------------------------
if years_compare:
    indicators = ["vehicles_million", "speed_kmh", "green_area", "population_million"]
    indicator_labels = {
        "vehicles_million": "รถยนต์",
        "speed_kmh": "ความเร็วเฉลี่ย",
        "green_area": "พื้นที่สีเขียว",
        "population_million": "ประชากร"
    }

    pastel_colors = ["#A5C8E1", "#AED9C4", "#EBC9D1", "#D5C3E8", "#FFE4A3", "#F7B7A3"]

    fig_bar = go.Figure()
    for idx, year in enumerate(years_compare):
        df_y = df[df["year"] == year]
        fig_bar.add_trace(go.Bar(
            name=str(year),
            x=[indicator_labels[i] for i in indicators],
            y=[df_y[i].values[0] for i in indicators],
            marker_color=pastel_colors[idx % len(pastel_colors)],
            text=[f"{df_y[i].values[0]:.2f}" for i in indicators],
            textposition="outside"
        ))

    fig_bar.update_layout(
        barmode="group",
        title=f"เปรียบเทียบตัวชี้วัดรายปี ({', '.join(map(str, years_compare))})",
        xaxis_title="ตัวชี้วัด (Indicator)",
        yaxis_title="ค่า (Value)",
        legend_title="ปี (Year)",
        bargap=0.25,
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        template="simple_white"
    )

    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("เลือกปีอย่างน้อย 1 ปีเพื่อแสดงกราฟเปรียบเทียบ")

st.markdown("---")

# -------------------------------------------------
# REAL KEPLER MAP
# -------------------------------------------------
st.subheader("📍 Bangkok Real Heatmap (Kepler.gl)")
kepler_url = "https://kepler.gl/demo/map?mapUrl=https://dl.dropboxusercontent.com/scl/fi/9alltkh7culor9ycmk5xu/keplergl_sfkt8ae.json?rlkey=g3h7t7ne3gm30ueobc33f3vp2&dl=0"
st.components.v1.iframe(kepler_url, height=600, width=1300, scrolling=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.caption("ข้อมูลจำลองเพื่อการศึกษา | © 2025 Bangkok Urban Dashboard | Source: BMA, DLT, TDRI (simulated)")
