"""
Sortino Ratio
--------------
Sortino ratio has been calculated for the year between 15th October 2020 and 15th October 2021.
This time period was chosen because of the date specified to use for the risk-free rate (15th October 2021)
"""

import yfinance as yf
import math
import pandas as pd

test_port_tickers = ["GLEN.L", "MRW.L", "AZN", "NKLA", "TSLA", "MSFT", "AMZN", "FNMA", "SPCE"]
port1_tickers = ["GLEN.L", "MRW.L", "AZN"]
port2_tickers = ["LGEN.L", "TSCO", "GSK"]

rfr = 0.0502  # Risk-free rate on 15th October 2021


def calculate_sortino(portfolio):
    """
    :param portfolio: Calculates portfolio sortino ratio using portfolio return, risk-free rate and downside risk

    :return: Returns portfolio sortino ratio. If downside risk == 0, sortino ratio is infinite and 0 is returned
    """
    portfolio_asset_returns = calculate_asset_returns(portfolio)  # Calculates asset returns in portfolio
    portfolio_return = calculate_portfolio_return(portfolio_asset_returns)  # Calculates average portfolio return
    downside_risk = calculate_downside_risk(portfolio_asset_returns)  # Calculates portfolio downside risk/deviation
    print("Risk-free rate is " + str(rfr))
    if downside_risk == 0:  # Handles downside risk = 0 to prevent division by zero error
        print("Sortino Ratio for portfolio is infinite(0)")
        print()
        return 0  # Infinite Sortino ratios are represented on graphs as 0
    else:
        sortino_ratio = ((portfolio_return - rfr) / downside_risk)  # Calculates sortino ratio for values received
        sortino_ratio = round(sortino_ratio, 4)  # Round sortino ratio to 4dp
        print("Sortino Ratio for portfolio is " + str(sortino_ratio))
        print()
        return sortino_ratio


def calculate_asset_returns(portfolio):
    """
    :param portfolio: Takes in list containing tickers as input, retrieves adjusted close data for specified dates and
    calculates asset return for each ticker in portfolio. Asset returns include dividend paid within time period.

    :return: List of asset returns for each ticker in portfolio
             Ticker and its asset return have the same index in their respective lists
    """
    asset_returns = list()
    for t in portfolio:
        ticker = yf.Ticker(t)
        asset_return = 0

        # Retrieves data for all dividend paid between 15/10/2020 and 16/10/2020
        dividend_data = ticker.dividends['2020-10-15':'2021-10-16']
        df = pd.DataFrame(dividend_data)
        for index, row in df.iterrows():  # Adds all dividend earned in time period to asset return
            asset_return += row["Dividends"]

        time_period = ticker.history(start="2020-10-15", end="2021-10-17")  # Retrieves data for specified time period
        start_date_close = time_period['Close']['2020-10-15']  # Retrieves adjusted close for start date (15/10/2020)
        end_date_close = time_period['Close']['2021-10-15']  # Retrieves adjusted close for end date (15/10/2021)

        asset_return += (end_date_close - start_date_close)
        asset_return = asset_return / start_date_close
        asset_returns.append(asset_return)  # Adds each asset's return to list
    return asset_returns  # Returns list with all asset returns


def calculate_portfolio_return(list_of_asset_returns):
    """
    :param list_of_asset_returns: Takes in a list of asset returns for an equally weighted portfolio and calculates
    actual or expected portfolio return

    :return: Calculated portfolio return
    """
    portfolio_return = 0
    portfolio_size = len(list_of_asset_returns)
    for i in list_of_asset_returns:
        portfolio_return += (i * (1 / portfolio_size))  # Calculates portfolio ratio of each asset with equal weighting
    print("Portfolio return is " + str(round(portfolio_return, 4)))
    return portfolio_return  # Returns portfolio performance with equally weighted assets


def calculate_downside_risk(list_of_asset_returns):
    """
    :param list_of_asset_returns: Calculates the standard deviation of assets with negative returns

    :return: Returns downside risk/deviation of negative asset returns
    """
    portfolio_size = len(list_of_asset_returns)
    total = 0
    for i in list_of_asset_returns:
        if i < 0:  # Squares and sums the values of negative asset returns
            total += (i * i)
    avg = total / portfolio_size  # Calculates the average of negative asset returns
    downside_risk = math.sqrt(avg)  # Calculates standard deviation by finding square root of average
    print("Downside risk is " + str(round(downside_risk, 4)))
    return downside_risk  # Returns downside risk/deviation


calculate_sortino(port1_tickers)
calculate_sortino(port2_tickers)
calculate_sortino(test_port_tickers)
