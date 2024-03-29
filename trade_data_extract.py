import yfinance as yf
import pandas as pd
import pandas.tseries.offsets as offsets

class FinanceData:
    def __init__(self, ticker, start, end):
        self.ticker = ticker.upper()
        self.start = pd.to_datetime(start) - pd.DateOffset(days=1)
        self.end = pd.to_datetime(end) + pd.DateOffset(days=1)
        self.data, self.return_plot_data, self.geometric_mean, self.price = self.load_data()

    def adjust_date_for_weekend(self, date):
        if not date.isoweekday() in range(1, 6):
            return pd.date_range(date - offsets.BDay(1), periods=1, freq="B")[0]
        return date

    def load_data(self):
        start_date = self.adjust_date_for_weekend(self.start)
        end_date = self.adjust_date_for_weekend(self.end)

        data = yf.download(self.ticker, start_date, end_date, progress=False, auto_adjust=True)
        price = data["Close"]
        daily_return = price.pct_change()
        return_plot_data = (price.pct_change()) * 100
        geometric_mean = (1 + daily_return).prod() - 1

        return data, return_plot_data, geometric_mean, price

    def calculate_interim_values(self, start_date, end_date, beginning_value, trades):
        interim_values, trade_dates = [], []
        market_value = beginning_value
        for trade in trades:
            trade_date = pd.to_datetime(trade["date"])
            if start_date <= trade_date <= end_date:
                shares_traded = trade["shares"]
                trade_data = self.data[self.data.index >= trade_date]
                if not trade_data.empty:
                    price_on_trade_date = trade_data.iloc[0]["Close"]
                    interim_market_value = ((market_value / trade_data.iloc[0]["Open"]) + shares_traded) * price_on_trade_date
                    interim_values.append(interim_market_value)
                    market_value = interim_market_value
                    trade_dates.append(trade_date)

        return interim_values, trade_dates
