# Online tool for calculating interim market values and holding period returns.

This document provides a comprehensive guide on the structure and functionality of the Interim market value tool, designed to calculate interim market values and holding period returns using Yahoo Finance data. The application is built with Python, utilizing `yfinance`, `pandas`, `plotly`, and `streamlit`.

## Overview

The application aims to provide users with an easy-to-use interface for analyzing financial securities over a specified period. It offers insights into the performance of stocks, including adjusted close prices, daily returns, and geometrically linked returns.

## Structure

The program is divided into two main components:

- `FinanceData` class: Handles data fetching, processing, and calculations.
- `StreamlitApp` class: Manages the user interface and interaction.

### `FinanceData` Class

Responsible for downloading and processing financial data from Yahoo Finance.

- **Methods**:
  - `__init__(self, ticker, start, end)`: Initializes the class with ticker symbol, start, and end dates.
  - `adjust_date_for_weekend(self, date)`: Adjusts dates to avoid weekends when the market is closed.
  - `load_data(self)`: Fetches the data from Yahoo Finance, calculates daily returns, and computes the geometric mean.
  - `calculate_interim_values(self, start_date, end_date, beginning_value, trades)`: Calculates interim market values based on user-defined trades.

### `StreamlitApp` Class

Creates an interactive web interface for users to input data and view results.

- **Methods**:
  - `__init__(self)`: Sets up the initial state of the application.
  - `setup_sidebar(self)`: Configures the sidebar with input fields for ticker symbol, dates, and trades.
  - `collect_trades(self)`: Gathers trade information from the user.
  - `display_user_manual(self)`: Displays instructions for using the application.
  - `display_results(self)`: Shows the results based on user inputs and calculations.
  - `plot_data(self, price, return_plot_data)`: Generates interactive plots of the adjusted close price and daily returns.

## Usage

1. **Input Parameters**: Users are prompted to enter the ticker symbol, analysis period (start and end dates), and details of any trades made within this period.
2. **Data Processing**: Upon submitting the inputs, the application calculates the interim market values, daily returns, and the geometric mean return for the period.
3. **Visualization and Output**: The results, including interactive plots and a summary of findings, are displayed on the web interface.

## Disclaimer

The data used in this application is sourced from Yahoo Finance and may not match the precision of paid data services. Results are to be considered as approximations for educational and proof-of-concept purposes only. Users should be aware of the limitations, especially regarding the accuracy of adjusted close prices for MFs and ETFs.

## Running the Application

# To run locally enter "streamlit run interim_mv_tool.py" in terminal and press enter.