import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MedChart Monitor", layout="wide")

st.title("🩺 MedChart Patient Vitals Monitor")

st.write("Upload a patient vitals dataset to visualize trends and detect alerts.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # alert logic
    def check_status(row):

        if row["heart_rate"] > 120 or row["heart_rate"] < 50:
            return "Critical"

        if row["systolic_bp"] > 160 or row["systolic_bp"] < 80:
            return "Critical"

        if row["temperature"] > 38.5 or row["temperature"] < 35:
            return "Critical"

        return "Normal"

    df["status"] = df.apply(check_status, axis=1)

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Heart Rate", round(df["heart_rate"].mean(),1))
    col2.metric("Avg BP", round(df["systolic_bp"].mean(),1))
    col3.metric("Avg Temp", round(df["temperature"].mean(),1))

    st.subheader("Heart Rate Trend")

    fig1 = px.line(
        df,
        x="timestamp",
        y="heart_rate",
        color="status",
        markers=True
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Blood Pressure Trend")

    fig2 = px.line(
        df,
        x="timestamp",
        y="systolic_bp",
        color="status",
        markers=True
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Temperature Trend")

    fig3 = px.line(
        df,
        x="timestamp",
        y="temperature",
        color="status",
        markers=True
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("🚨 Alerts")

    alerts = df[df["status"]=="Critical"]

    if len(alerts) > 0:
        st.error("Critical readings detected")
        st.dataframe(alerts)
    else:
        st.success("All vitals normal")

else:
    st.info("Upload a CSV file to start monitoring.")