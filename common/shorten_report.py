from typing import Dict

from stock_analysis.models import StockSymbolReport


def get_shortened_stock_symbol_report(report: StockSymbolReport) -> Dict:
    # This is a temporary function that will clean the data until I write it cleaner in the first place.
    report_dict = report.dict()
    data = report_dict["data"]
    cleaned_data = {
        'industry': data.get('industry'),
        'sector': data.get('sector'),
        'fullTimeEmployees': data.get('fullTimeEmployees'),
        'previousClose': data.get('previousClose'),
        'open': data.get('open'),
        'dayLow': data.get('dayLow'),
        'dayHigh': data.get('dayHigh'),
        'regularMarketVolume': data.get('regularMarketVolume'),
        'marketCap': data.get('marketCap'),
        'fiftyTwoWeekLow': data.get('fiftyTwoWeekLow'),
        'fiftyTwoWeekHigh': data.get('fiftyTwoWeekHigh'),
        'twoHundredDayAverage': data.get('twoHundredDayAverage'),
        'trailingAnnualDividendYield': data.get('trailingAnnualDividendYield'),
        'sharesShort': data.get('sharesShort'),
        'heldPercentInstitutions': data.get('heldPercentInstitutions'),
        'pegRatio': data.get('pegRatio'),
        'exchange': data.get('exchange'),
        'symbol': data.get('symbol'),
        'underlyingSymbol': data.get('underlyingSymbol')
    }
    report_dict["data"] = cleaned_data
    del report_dict["news_report"]["articles_summary"]
    return report_dict
