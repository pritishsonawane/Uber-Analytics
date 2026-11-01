
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Uber Rides Analytics",
    page_icon="🚕",
    layout="wide"
)

st.title("🚕 Uber Rides Analytics Dashboard")
st.caption("Business Intelligence and Predictive Analytics")

uploaded = st.sidebar.file_uploader(
    "Upload Uber CSV dataset",
    type=["csv"]
)

if uploaded is not None:
    df = pd.read_csv(uploaded)
elif __import__("os").path.exists("uber_cleaned_data.csv"):
    df = pd.read_csv("uber_cleaned_data.csv")
else:
    st.warning("Upload your Uber CSV dataset to begin.")
    st.stop()

st.sidebar.header("Dashboard Filters")

if "Booking Status" in df.columns:
    statuses = df["Booking Status"].dropna().unique().tolist()
    selected = st.sidebar.multiselect(
        "Booking Status",
        statuses,
        default=statuses
    )
    df = df[df["Booking Status"].isin(selected)]

if "Vehicle Type" in df.columns:
    vehicles = df["Vehicle Type"].dropna().unique().tolist()
    selected_vehicles = st.sidebar.multiselect(
        "Vehicle Type",
        vehicles,
        default=vehicles
    )
    df = df[df["Vehicle Type"].isin(selected_vehicles)]

total = len(df)
completed = (
    (df["Booking Status"] == "Completed").sum()
    if "Booking Status" in df.columns else 0
)
completion = completed / total * 100 if total else 0

revenue = (
    df["Booking Value"].sum()
    if "Booking Value" in df.columns else 0
)

distance = (
    df["Ride Distance"].mean()
    if "Ride Distance" in df.columns else 0
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Bookings", f"{total:,}")
c2.metric("Completed Rides", f"{completed:,}")
c3.metric("Completion Rate", f"{completion:.1f}%")
c4.metric("Booking Value", f"{revenue:,.0f}")

st.divider()

if "Booking Status" in df.columns:
    st.subheader("Booking Status Analysis")
    a, b = st.columns(2)

    status = df["Booking Status"].value_counts().reset_index()
    status.columns = ["Status", "Bookings"]

    a.plotly_chart(
        px.pie(status, names="Status", values="Bookings",
               title="Booking Status Distribution"),
        use_container_width=True
    )

    b.plotly_chart(
        px.bar(status, x="Status", y="Bookings",
               title="Bookings by Status"),
        use_container_width=True
    )

if "Vehicle Type" in df.columns:
    st.subheader("Vehicle Analysis")
    vehicle = df["Vehicle Type"].value_counts().reset_index()
    vehicle.columns = ["Vehicle", "Bookings"]

    st.plotly_chart(
        px.bar(vehicle, x="Vehicle", y="Bookings",
               title="Bookings by Vehicle Type"),
        use_container_width=True
    )

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    monthly = (
        df.dropna(subset=["Date"])
        .groupby(df["Date"].dt.to_period("M"))
        .size().reset_index(name="Bookings")
    )
    monthly["Month"] = monthly.iloc[:, 0].astype(str)

    st.subheader("Monthly Booking Trend")
    st.plotly_chart(
        px.line(monthly, x="Month", y="Bookings",
                markers=True, title="Monthly Bookings"),
        use_container_width=True
    )

if "Pickup Location" in df.columns:
    st.subheader("Top Pickup Locations")
    pickup = df["Pickup Location"].value_counts().head(10).reset_index()
    pickup.columns = ["Location", "Bookings"]

    st.plotly_chart(
        px.bar(pickup, x="Bookings", y="Location",
               orientation="h"),
        use_container_width=True
    )

st.subheader("Dataset Explorer")
st.dataframe(df, use_container_width=True)

st.download_button(
    "Download Filtered Data",
    df.to_csv(index=False).encode("utf-8"),
    "uber_filtered_data.csv",
    "text/csv"
)

st.success("Dashboard loaded successfully!")
