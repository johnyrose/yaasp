import yfinance as yf

from data_collection.models import CompanyStockInfo


def get_stock_info(company_symbol: str) -> CompanyStockInfo:
    ticker = yf.Ticker(company_symbol)
    info = ticker.info
    return CompanyStockInfo(
        industry=info.get('industry', ''),
        sector=info.get('sector', ''),
        fullTimeEmployees=info.get('fullTimeEmployees', 0),
        previousClose=info.get('regularMarketPreviousClose', 0),
        open=info.get('regularMarketOpen', 0),
        dayLow=info.get('regularMarketDayLow', 0),
        dayHigh=info.get('regularMarketDayHigh', 0),
        regularMarketVolume=info.get('regularMarketVolume', 0),
        marketCap=info.get('marketCap', 0),
        fiftyTwoWeekLow=info.get('fiftyTwoWeekLow', 0),
        fiftyTwoWeekHigh=info.get('fiftyTwoWeekHigh', 0),
        twoHundredDayAverage=info.get('twoHundredDayAverage', 0),
        trailingAnnualDividendYield=info.get('trailingAnnualDividendYield', 0),
        sharesShort=info.get('sharesShort', 0),
        heldPercentInstitutions=info.get('heldPercentInstitutions', 0),
        pegRatio=info.get('pegRatio', 0),
        exchange=info.get('exchange', ''),
        symbol=info.get('symbol', ''),
        underlyingSymbol=info.get('underlyingSymbol', ''),
        description=info.get('longName', ''),
        bid=info.get('bid', 0),
        ask=info.get('ask', 0),
        last=info.get('regularMarketPrice', 0),
        change=info.get('regularMarketChange', 0),
        days_range=f"{info.get('regularMarketDayLow', 0)}-{info.get('regularMarketDayHigh', 0)}",
        fifty_two_week_range=f"{info.get('fiftyTwoWeekLow', 0)}-{info.get('fiftyTwoWeekHigh', 0)}",
        volume=info.get('regularMarketVolume', 0),
        avg_volume=info.get('averageDailyVolume10Day', 0),
        pe_ratio=info.get('trailingPE', 0),
        eps=info.get('trailingEps', 0),
        earnings_date=info.get('earningsTimestamp', ''),
        dividend=info.get('dividendRate', 0),
        dividend_yield=info.get('dividendYield', 0),
        ex_dividend_date=info.get('exDividendDate', '')
    )
