import streamlit as st
from trade_data_extract import FinanceData
import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots

class StreamlitApp:
    def __init__(self):
        self.setup_sidebar()
        self.finance_data = None

    def setup_sidebar(self):
        st.sidebar.header("Fund Parameters")
        self.ticker = st.sidebar.text_input("Ticker").upper()
        self.start_date = st.sidebar.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=365))
        self.end_date = st.sidebar.date_input("End Date", datetime.date.today())
        self.beginning_value = st.sidebar.number_input("Beginning Market Value", min_value=0.01, step=0.01)
        self.trades = self.collect_trades()

    def collect_trades(self):
        trades = []
        for i in range(4):
            trade_date = st.sidebar.date_input(f"Trade {i+1} Date", self.start_date + datetime.timedelta(days=30 * (i + 1)))
            shares = st.sidebar.number_input(f"Number of Shares for Trade {i+1}", min_value=0)
            trades.append({"date": trade_date, "shares": shares})
        return trades

    def display_user_manual(self):
        st.write(
            """
            ### User Manual
            * Enter a Ticker, start date, & end date for the period.
                * Enter the BMV, trade dates, & shares traded to return interim market value(s) as needed.
            * Press the 'Get Data' button below to display your return & interactive security data.
            """
        )

    def display_results(self):
        self.display_user_manual()  # Display user manual at the beginning
        if st.button("Get Data") and self.ticker:
            st.title("A simple web app for calculating returns and interim market values")
            self.finance_data = FinanceData(self.ticker, self.start_date, self.end_date)
            interim_values, trade_dates = self.finance_data.calculate_interim_values(self.start_date, self.end_date, self.beginning_value, self.trades)
            
            st.markdown(f"**{self.ticker} return from {self.start_date} to {self.end_date}: {self.finance_data.geometric_mean:.4%}**")
            
            if interim_values:
                st.write("Interim Market Value(s):")
                for i, value in enumerate(interim_values):
                    st.write(f"{trade_dates[i].date()}: ${value:.2f}")

            # Plotting
            fig = self.plot_data(self.finance_data.price, self.finance_data.return_plot_data)
            st.plotly_chart(fig, use_container_width=True)

    def plot_data(self, price, return_plot_data):
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)
        fig.add_trace(go.Scatter(x=price.index, y=price.values, name="Adjusted Close Price"), row=1, col=1)
        fig.add_trace(go.Scatter(x=return_plot_data.index, y=return_plot_data.values, name="Daily Return"), row=2, col=1)

        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Adjusted Close Price", row=1, col=1)
        fig.update_yaxes(title_text="Daily Return", row=2, col=1)
        fig.update_layout(title=f"Daily {self.ticker} Price and Returns: {self.start_date} to {self.end_date}")
        
        return fig
