import finnhub
import yfinance as yf

from common.logger import logger
from config import FINNHUB_API_KEY
from common.models.data_collection import CompanyStockInfo


def get_company_name_from_symbol(company_symbol: str) -> str:
    ticker_info = yf.Ticker(company_symbol).info
    company_name = ticker_info['longName']
    return company_name


def get_stock_info(company_symbol: str) -> CompanyStockInfo:
    logger.info(f"Getting stock financial info for {company_symbol}...")
    ticker = yf.Ticker(company_symbol)
    info = ticker.info

    try:
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        company_earnings = finnhub_client.company_earnings(symbol=company_symbol)
    except Exception as e:
        logger.warning(f"Failed to get earnings for {company_symbol} - {e}. The stock info won't include it.")
        company_earnings = None

    return CompanyStockInfo(
        industry=info.get('industry', ''),
        sector=info.get('sector', ''),
        company_earnings=company_earnings,
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
