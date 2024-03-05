import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style="dark")

day_df = pd.read_csv("./data/clean_day.csv")
day_df.head()


def generate_daily_rent_df(df):
    daily_rent_df = df.groupby("dteday").agg({"count": "sum"}).reset_index()
    return daily_rent_df


def generate_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby("dteday").agg({"casual": "sum"}).reset_index()
    return daily_casual_rent_df


def generate_daily_registered_rent_df(df):
    daily_registered_rent_df = (
        df.groupby("dteday").agg({"registered": "sum"}).reset_index()
    )
    return daily_registered_rent_df


def generate_season_rent_df(df):
    season_rent_df = df.groupby("season")[["registered", "casual"]].sum().reset_index()
    return season_rent_df


def generate_monthly_rent_df(df):
    monthly_rent_df = df.groupby(["month", "year"]).agg({"count": "sum"}).reset_index()
    ordered_months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    monthly_rent_df = monthly_rent_df.sort_values(
        by=["year", "month"],
        key=lambda x: x.map({v: i for i, v in enumerate(ordered_months)}),
    )
    return monthly_rent_df


def generate_weekday_rent_df(df):
    weekday_rent_df = df.groupby("weekday").agg({"count": "sum"}).reset_index()
    return weekday_rent_df


def generate_workingday_rent_df(df):
    workingday_rent_df = df.groupby("workingday").agg({"count": "sum"}).reset_index()
    return workingday_rent_df


def generate_holiday_rent_df(df):
    holiday_rent_df = df.groupby("holiday").agg({"count": "sum"}).reset_index()
    return holiday_rent_df


def generate_weather_rent_df(df):
    weather_rent_df = df.groupby("weather_situation").agg({"count": "sum"})
    return weather_rent_df


min_date = pd.to_datetime(day_df["dteday"]).dt.date.min()
max_date = pd.to_datetime(day_df["dteday"]).dt.date.max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

main_df = day_df[
    (day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))
]

# Generate Dataframe
daily_rent_df = generate_daily_rent_df(main_df)
daily_casual_rent_df = generate_daily_casual_rent_df(main_df)
daily_registered_rent_df = generate_daily_registered_rent_df(main_df)
season_rent_df = generate_season_rent_df(main_df)
monthly_rent_df = generate_monthly_rent_df(main_df)
weekday_rent_df = generate_weekday_rent_df(main_df)
workingday_rent_df = generate_workingday_rent_df(main_df)
holiday_rent_df = generate_holiday_rent_df(main_df)
weather_rent_df = generate_weather_rent_df(main_df)


# Dashboard

st.header("Bike Rental Dashboard")

st.subheader("Daily Rentals")
col1, col2, col3 = st.columns(3)
col1.metric("Casual User", value=daily_casual_rent_df["casual"].sum())
col2.metric("Registered User", value=daily_registered_rent_df["registered"].sum())
col3.metric("Total User", value=daily_rent_df["count"].sum())

st.subheader("Monthly Rentals")
fig, ax = plt.subplots(figsize=(24, 8))
for year, data in monthly_rent_df.groupby("year"):
    ax.plot(data["month"], data["count"], marker="o", label=year)
ax.set_title("Jumlah sepeda yang disewakan berdasarkan Bulan dan tahun")
ax.tick_params(axis="x", labelsize=25, rotation=45)
ax.tick_params(axis="y", labelsize=20)
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

st.subheader("Rentals by Season")
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x="season",
    y="registered",
    data=season_rent_df,
    label="Registered",
    ax=ax,
)
sns.barplot(
    x="season",
    y="casual",
    data=season_rent_df,
    label="Casual",
    ax=ax,
)
for index, row in season_rent_df.iterrows():
    ax.text(
        index,
        row["registered"],
        str(row["registered"]),
        ha="center",
        va="bottom",
        fontsize=12,
    )
    ax.text(
        index, row["casual"], str(row["casual"]), ha="center", va="bottom", fontsize=12
    )
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis="x", labelsize=20, rotation=0)
ax.tick_params(axis="y", labelsize=15)
ax.legend()
st.pyplot(fig)

st.subheader("Rentals by Weather")
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x=weather_rent_df.index, y=weather_rent_df["count"], ax=ax)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis="x", labelsize=20)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

st.subheader("Holiday and Rentals by Day")
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))

sns.barplot(x="holiday", y="count", data=holiday_rent_df, hue="holiday", ax=axes[0])
axes[0].set_title("Number of Rents based on Holiday")
axes[0].set_ylabel(None)
axes[0].tick_params(axis="x", labelsize=15)
axes[0].tick_params(axis="y", labelsize=10)

sns.barplot(x="weekday", y="count", data=weekday_rent_df, hue="weekday", ax=axes[1])
axes[1].set_title("Number of Rents based on Weekday")
axes[1].set_ylabel(None)
axes[1].tick_params(axis="x", labelsize=15)
axes[1].tick_params(axis="y", labelsize=10)

st.pyplot(fig)
st.caption("Ahmad Sultani Dayanullah")
