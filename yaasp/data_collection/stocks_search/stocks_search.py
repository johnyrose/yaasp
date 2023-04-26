# This section might be used in the future.
# Taken from: https://towardsdatascience.com/making-a-stock-screener-with-python-4f591b198261
from typing import List

import requests
from bs4 import BeautifulSoup
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
import yfinance as yf
import datetime
import time
import csv


def get_sp500_companies_tickers() -> List[str]:
    #  This is a very hacky and dirty way to get the companies, but it'll do for now
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    sp500_table = soup.find("table", {"class": "wikitable"})
    sp500_rows = sp500_table.find_all("tr")[1:]  # Skip the header row

    companies = []
    for row in sp500_rows:
        columns = row.find_all("td")
        ticker = columns[0].text.strip()
        name = columns[1].text.strip()
        companies.append({"ticker": ticker, "name": name})

    return [company['ticker'] for company in companies]


index_symbols = {
    'S&P 500': '^GSPC',
    'NASDAQ 100': '^NDX',
    'DOW 30': '^DJI',
    # Add more index symbols here as needed
}


index_to_function = {
    'S&P 500': get_sp500_companies_tickers(),
    'DOW 30': si.tickers_dow(),
}


def get_stock_tickers(index: str) -> List[str]:
    if index in index_to_function:
        return index_to_function[index]
    else:
        raise ValueError(f"Index '{index}' not supported.")


def perform_minervini_conditions_check(stocks_list: List, export_list: List, returns_multiples):
    for stock, returns_multiple in stocks_list:
        try:
            with open(f'csvs/{stock}.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                df = [row for row in reader]

            sma = [50, 150, 200]
            for x in sma:
                for i in range(len(df) - x + 1):
                    sma_sum = sum(float(row['Adj Close']) for row in df[i:i + x])
                    df[i + x - 1][f"SMA_{x}"] = sma_sum / x

            # Storing required values
            current_close = float(df[-1]["Adj Close"])
            moving_average_50 = float(df[-1]["SMA_50"])
            moving_average_150 = float(df[-1]["SMA_150"])
            moving_average_200 = float(df[-1]["SMA_200"])
            low_of_52week = min(float(row["Low"]) for row in df[-260:])
            high_of_52week = max(float(row["High"]) for row in df[-260:])
            RS_Rating = round((returns_multiple / max(returns_multiples, key=lambda x: x[1])[1]) * 100)

            try:
                moving_average_200_20 = float(df[-20]["SMA_200"])
            except Exception:
                moving_average_200_20 = 0

            # Condition 1: Current Price > 150 SMA and > 200 SMA
            condition_1 = current_close > moving_average_150 > moving_average_200

            # Condition 2: 150 SMA and > 200 SMA
            condition_2 = moving_average_150 > moving_average_200

            # Condition 3: 200 SMA trending up for at least 1 month
            condition_3 = moving_average_200 > moving_average_200_20

            # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
            condition_4 = moving_average_50 > moving_average_150 > moving_average_200

            # Condition 5: Current Price > 50 SMA
            condition_5 = current_close > moving_average_50

            # Condition 6: Current Price is at least 30% above 52 week low
            condition_6 = current_close >= (1.3 * low_of_52week)

            # Condition 7: Current Price is within 25% of 52 week high
            condition_7 = current_close >= (.75 * high_of_52week)

            # If all conditions above are true, add stock to exportList
            if (
                    condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7):
                export_list.append({"Stock": stock, "RS_Rating": RS_Rating, "50 Day MA": moving_average_50,
                                    "150 Day Ma": moving_average_150, "200 Day MA": moving_average_200,
                                    "52 Week Low": low_of_52week, "52 week High": high_of_52week})
                print(stock + " made the Minervini requirements")
        except Exception as e:
            print(e)
            print(f"Could not gather data on {stock}")


def find_stocks(index: str):
    yf.pdr_override()

    # Variables
    tickers = get_stock_tickers(index)
    tickers = [item.replace(".", "-") for item in tickers]  # Yahoo Finance uses dashes instead of dots
    index_name = index_symbols[index]

    start_date = datetime.datetime.now() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    export_list = []

    returns_multiples = []

    # Index Returns
    index_df = pdr.get_data_yahoo(index_name, start_date, end_date)
    index_df['Percent Change'] = index_df['Adj Close'].pct_change()
    index_return = (index_df['Percent Change'] + 1).cumprod()[-1]

    # Find top 30% performing stocks (relative to the S&P 500)
    for ticker in tickers:
        try:
            # Download historical data as CSV for each stock (makes the process faster)
            df = pdr.get_data_yahoo(ticker, start_date, end_date)
            df.to_csv(f'csvs/{ticker}.csv')

            # Calculating returns relative to the market (returns multiple)
            df['Percent Change'] = df['Adj Close'].pct_change()
            stock_return = (df['Percent Change'] + 1).cumprod()[-1]

            returns_multiple = round((stock_return / index_return), 2)
            returns_multiples.append((ticker, returns_multiple))

            print(f'Ticker: {ticker}; Returns Multiple against S&P 500: {returns_multiple}\n')
            time.sleep(1)
        except Exception:
            print(f'Could not gather data on {ticker}')

    # Creating a list of only top 30%
    returns_multiples.sort(key=lambda x: x[1], reverse=True)
    cutoff = int(len(returns_multiples) * 0.3)
    top_stocks = returns_multiples[:cutoff]

    # Checking Minervini conditions of top 30% of stocks in given list
    perform_minervini_conditions_check(top_stocks, export_list, returns_multiples)

    export_list.sort(key=lambda x: x['RS_Rating'], reverse=True)
    return export_list
