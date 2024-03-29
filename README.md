# Online tool for calculating interim market values and holding period returns.

Disclaimer: the data stream that feeds into this app is from the yahoo finance API which is a free data source and may not be as accurate as other paid-for services. This may cause noticable differences in calculated returns when compared to other data vendors. The resulting values generated by this model are approximations at best and this is solely presented as a proof-of-concept project. Accuracy has been improved in terms of pricing, however the adjusted close price for MFs and ETFs are not actually accounting for income accrual events. These income accruals will have to be scraped from yfinance to ensure calculated returns are accurate for all periods.

## Set up:
* Import necessary packages
* initialize notebook mode and go offline for cufflinks wrapper on plotly vizuals, this combination allows for interactive plots
* Use streamlit @st_cache_data decorator to allows streamlit to run the function in the .py file and store the return value in a cache. The next time the function is called with the same parameters and code (e.g., when a user interacts with the app), Streamlit will skip executing the function altogether and return the cached value instead.
* During development, the cache updates automatically as the function code changes, ensuring that the latest changes are reflected in the cache.
* The @st_cache_data decorator is the recommended way to cache computations that return data: loading a DataFrame from CSV, transforming a NumPy array, querying an API, or any other function that returns a serializable data object (str, int, float, DataFrame, array, list, …). It creates a new copy of the data at each function call, making it safe against mutations and race conditions. 

## load_data function:
* Takes three arguments: symbol, start, and end. 
* The purpose of the function is to download security price data for a given ticker, calculate the holding period return, and summary statistics for the data.
* The function first checks if the "symbol" argument is empty or not. 
* If the "symbol" is empty, the function prints an error message using st.error() function and returns None for all of its return values. 
* If "symbol" is not empty, the function continues to download the security price data using the Yahoo Finance API, yf.download(). 
* The function downloads the Close price of the chosen security from the given start and end dates, and assigns it to the variable price. The auto-adjust argument in the yf.download() function is set to true to adjust the security price for any income accrual events within the period.
* Next, the function calculates the daily returns of the security using the pct_change() function from Pandas library. It also calculates the returns multiplied by 100 to display a percentage value, and assigns the result to the variable return_plot_data which feeds feed into the interactive plots and data table at the end of this script.
* The function then calculates the geometric (TTWR) of the daily returns using the formula geometric_mean = ((((1 + daily_return)).prod()) - 1). This formula calculates the compounded daily return over the given period, and subtracts 1 from the result to get the total return over the period. Geometrically linked or TTWR is a commonly used measure of investment performance.
* Finally, the function returns the four values: the downloaded data from Yahoo Finance, the return_plot_data, the geometric_mean, and the price.

## calculate_interim_values function:
* Takes four arguments: data, start_date, end_date, and beginning_value. 
* The purpose of the function is to calculate the market values of a security over a series of trades made within a given holding period, based on user inputs.
* The function first creates an empty list called trades. It then loops over four iterations (represented by the range 4) and prompts the user to input a trade date using the st.sidebar.date_input() function. 
* If the input trade date is within the specified time period, the function prompts the user to input the number of shares for that trade, and creates a dictionary called trade with the trade date and number of shares as key-value pairs. The trade dictionary is then appended to the trades list.
* The function then creates an empty list called interim_values and initializes a variable market_value with the beginning_value. 
* It then loops over each trade in the trades list, and calculates the market value of the security based on the number of shares traded and the price on the trade date. If there were shares traded on the trade date, the function first converts the trade date to a Pandas Timestamp object, and extracts the subset of data containing all rows with a timestamp greater than or equal to the trade date. 
* It then calculates the price of the security on the trade date using the Close price from data.
* The interim market value is calculated using the formula ((market_value / trade_data.iloc[0]['Open']) + shares_traded) * price_on_trade_date. 
* The interim market value is added to the interim_values list, and the variable market_value is updated to the interim market value.
* This function returns two values: the interim_values list containing the market values at each trade, and a list of the trade dates.

## Setting up the user interface for the streamlit app:
* Sets up the user interface for a web app to calculate returns and interim market values for a security. The Streamlit library is used to create an interactive sidebar and main display area.
* The first few lines of code define the sidebar, which contains user input fields for the ticker, start and end dates, and optional parameters for calculating interim market values. 
* The st.sidebar.text_input() function prompts the user to enter a ticker symbol.
* The st.sidebar.date_input() function prompts the user to enter a start and end date for the analysis period. 
* The optional parameters for calculating interim market values include fields for entering trade dates and shares traded.
* The if statement checks whether the start date is earlier than the end date. If the start date is later than the end date, an error message is displayed using the st.sidebar.error() function.
* The st.title() and st.write() functions define the main display area of the web app. The st.title() function displays a large text header, while the st.write() function displays an instruction manual for using the web app. 
* The manual provides step-by-step instructions for entering inputs and getting results from the app.

## Get data button:
* The script then calls the load_data() function, passing in the ticker and start and end dates as arguments, and assigns the returned values to data, return_plot_data, geometric_mean, and price. 
* The user is prompted to input a beginning market value using st.sidebar.number_input() 
* The calculate_interim_values() function is called to calculate any interim market values and trade dates based on the user's input.
* If the user clicks the "Get Data" button, the geometric return for the time period, any interim market values and trade dates (if applicable), and a plot of the daily adjusted close price and daily return for the time period are displayed using st.write() and st.plotly_chart().

## Plotting and displaying interactive data:
* A plot is created, using the plotly library for creating interactive subplots of the price timeseries and daily return movements. 
* The two subplots two subplots are stacked vertically, with a shared x-axis. The top subplot shows the adjusted close price of the security over the selected date range, while the bottom subplot shows the daily return of the security over the same date range.
* The make_subplots function is used to create the two subplots, with rows=2 and cols=1 indicating that we want two subplots stacked vertically. 
* The shared_xaxes=True argument ensures that the two subplots share the same x-axis. The vertical_spacing argument sets the vertical spacing between the two subplots.
* The add_trace method is used twice to add traces to the subplots. In the first call, a Scatter object is added to the top subplot with the adjusted close price data using the price DataFrame.
* In the second call, another Scatter object is added to the bottom subplot with the daily return data using the return_plot_data DataFrame.
* The update_xaxes and update_yaxes methods are used to add axis titles to the subplots. 
* The update_layout method is used to add a title to the entire plot.
* Finally, the plotly_chart function is used to render the plot in the Streamlit app. 
* The use_container_width=True argument makes the plot fill the entire width of the container it is in on streamlit app webpage.
* After the plot is displayed, the "data" DataFrame is modified to remove the time component of the date index and set the date as the index of the DataFrame. 
* The modified price DataFrame is displayed in the left column of a two-column layout, while the output of price.describe() is displayed in the right column.


