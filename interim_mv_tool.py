import yfinance as yf
import streamlit as st
import datetime
import pandas as pd
import pandas.tseries.offsets as offsets
import numpy as np
import cufflinks as cf
from plotly.offline import iplot, init_notebook_mode
from plotly.subplots import make_subplots
import plotly.graph_objs as go

init_notebook_mode(connected=True)
cf.go_offline()


@st.cache_data
def load_data(ticker, start, end):
    if not ticker:
        st.error("Please enter a valid ticker")
        return None, None, None, None

    start_date = pd.to_datetime(start) - pd.DateOffset(days=1)
    if not start_date.isoweekday() in range(1, 5):
        start_date = pd.date_range(start_date - offsets.BDay(1), periods=1, freq="B")[0]

    end_date = pd.to_datetime(end) + pd.DateOffset(days=1)
    if not end_date.isoweekday() in range(1, 5):
        end_date = pd.date_range(end_date, periods=1, freq="B")[0]

    data = yf.download(ticker, start_date, end_date, progress=False, auto_adjust=True)
    price = yf.download(ticker, start_date, end_date, progress=False, auto_adjust=True)[
        "Close"
    ]
    # Calculate daily return
    daily_return = price.pct_change()

    # Plot the daily return movements
    return_plot_data = (price.pct_change()) * 100

    # Geometrically link all daily returns for the period chose
    geometric_mean = (1 + daily_return).prod() - 1

    return data, return_plot_data, geometric_mean, price


def calculate_interim_values(data, start_date, end_date, beginning_value):
    trades = []
    for i in range(4):
        trade_date = st.sidebar.date_input(
            f"Trade {i+1} Date", start_date + datetime.timedelta(days=30 * (i + 1))
        )
        if start_date <= trade_date <= end_date:
            shares = st.sidebar.number_input(f"Number of Shares for Trade {i+1}")
            trade = {"date": trade_date, "shares": shares}
            trades.append(trade)

    interim_values = []
    market_value = beginning_value
    for trade in trades:
        shares_traded = trade["shares"]
        if shares_traded:
            trade_date = pd.to_datetime(trade["date"]).tz_localize("America/New_York")
            trade_data = data[
                pd.to_datetime(data.index).tz_localize(None)
                >= pd.Timestamp(trade_date).tz_localize(None)
            ]
            price_on_trade_date = trade_data.iloc[0]["Close"]
            interim_market_value = (
                (market_value / trade_data.iloc[0]["Open"]) + shares_traded
            ) * price_on_trade_date
            interim_values.append(interim_market_value)
            market_value = interim_market_value

    return interim_values, [trade["date"] for trade in trades]


st.sidebar.header("Fund Parameters")

ticker = st.sidebar.text_input("Ticker").upper()

start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Validate input
if start_date is not None and end_date is not None:
    if start_date > end_date:
        st.sidebar.error("Error: End date must fall after start date.")


st.title("A simple web app for calculating returns and interim market values")

st.write(
    """
    ### User Manual
    * Enter a Ticker, start date, & end date for the period.
        * Enter the BMV, trade dates, & shares traded to return interim market value(s) as needed.
    * Press the 'Get Data' button below to display your return & interactive security data.
"""
)

data, return_plot_data, geometric_mean, price = load_data(ticker, start_date, end_date)
beginning_value = st.sidebar.number_input(
    "Beginning Market Value", min_value=0.01, step=0.01
)
interim_values, trade_dates = calculate_interim_values(
    data, start_date, end_date, beginning_value
)

if st.button("Get Data"):

    if ticker:

        st.write(
            f"<b>{ticker} return from {start_date} to {end_date}: {geometric_mean:.4%}</b>",
            unsafe_allow_html=True,
        )

        if len(interim_values) > 0:
            st.write("Interim Market Value(s):")
            for i, value in enumerate(interim_values):
                st.write(f"{trade_dates[i]}: ${value:.2f}")

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)

        fig.add_trace(
            go.Scatter(x=price.index, y=price.values, name="Adjusted Close Price"),
            row=1,
            col=1,
        )

    fig.add_trace(
        go.Scatter(
            x=return_plot_data.index, y=return_plot_data.values, name="Daily Return"
        ),
        row=2,
        col=1,
    )

    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Adjusted Close Price", row=1, col=1)
    fig.update_yaxes(title_text="Daily Return", row=2, col=1)

    fig.update_layout(
        title=f"Daily {ticker} Price and Returns: {start_date} to {end_date}"
    )

    st.plotly_chart(fig, use_container_width=True)

    data = data.reset_index()  # move date and time to axis 1 index 0
    data["Date"] = pd.to_datetime(
        data["Date"]
    )  # Convert 'Date' column to datetime type
    date = data["Date"].dt.date  # Access the date portion of the datetime values
    ex_dt = data.iloc[:, 1:]  # create new date only index column
    price_table = ex_dt.set_index(date)  # set date column
    col1, col2 = st.columns(2)
    with col1:
        st.write(price)
    with col2:
        st.write(price.describe())

# To run locally enter "streamlit run interim_mv_tool.py" in terminal and press enter.
