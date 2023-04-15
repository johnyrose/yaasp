from typing import Dict

from stock_analysis.models import StockSymbolReport


def get_shortened_stock_symbol_report(report: StockSymbolReport) -> Dict:
    # This is a temporary function that will clean the data until I write it cleaner in the first place.
    report_dict = report.dict()
    data = report_dict["data"]
    cleaned_data = {
        'industry': data['industry'],
        'sector': data['sector'],
        'fullTimeEmployees': data['fullTimeEmployees'],
        'previousClose': data['previousClose'],
        'open': data['open'],
        'dayLow': data['dayLow'],
        'dayHigh': data['dayHigh'],
        'regularMarketVolume': data['regularMarketVolume'],
        'marketCap': data['marketCap'],
        'fiftyTwoWeekLow': data['fiftyTwoWeekLow'],
        'fiftyTwoWeekHigh': data['fiftyTwoWeekHigh'],
        'twoHundredDayAverage': data['twoHundredDayAverage'],
        'trailingAnnualDividendYield': data['trailingAnnualDividendYield'],
        'sharesShort': data['sharesShort'],
        'heldPercentInstitutions': data['heldPercentInstitutions'],
        'pegRatio': data['pegRatio'],
        'exchange': data['exchange'],
        'symbol': data['symbol'],
        'underlyingSymbol': data['underlyingSymbol']
    }
    report_dict["data"] = cleaned_data
    del report_dict["news_report"]["articles_summary"]
    return report_dict
