import yfinance as yf

from data_collection.models import CompanyStockInfo


def get_stock_info(company_symbol: str) -> CompanyStockInfo:
    ticker = yf.Ticker(company_symbol)
    info = ticker.info

    if not info:
        raise Exception(f'Could not get stock info for {company_symbol}')

    company_stock_info = CompanyStockInfo(
        symbol=info.get('symbol', ''),
        description=info.get('longName', ''),
        bid=info.get('bid', 0),
        ask=info.get('ask', 0),
        last=info.get('regularMarketPrice', 0),
        change=info.get('regularMarketChange', 0),
        days_range=f"{info.get('regularMarketDayLow', 0)} - {info.get('regularMarketDayHigh', 0)}",
        fifty_two_week_range=f"{info.get('fiftyTwoWeekLow', 0)} - {info.get('fiftyTwoWeekHigh', 0)}",
        volume=info.get('regularMarketVolume', 0),
        avg_volume=info.get('averageDailyVolume3Month', 0),
        market_cap=info.get('marketCap', 0),
        pe_ratio=info.get('trailingPE', 0),
        eps=info.get('trailingEps', 0),
        earnings_date=info.get('earningsTimestamp', ''),
        dividend=info.get('dividendRate', 0),
        dividend_yield=info.get('dividendYield', 0),
        ex_dividend_date=info.get('exDividendDate', ''),
        one_year_target_estimate=info.get('targetMeanPrice', 0),
    )

    return company_stock_info
