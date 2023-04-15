import json

from data_collection.company_stock_data_collector import get_stock_info
from data_collection.news_collection.marketaux_collector import MarketauxNewsCollector
from data_collection.news_collection.news_api_collector import NewsAPICollector
from stock_analysis.models import StockSymbolReport
from stock_analysis.news_report_generator import generate_news_report
from stock_analysis.stock_symbol_report_generator import generate_stock_symbol_report


def generate_stock_report(stock_symbol: str) -> StockSymbolReport:
    news_api_articles = NewsAPICollector(stock_symbol).get_news_articles()
    marketaux_articles = MarketauxNewsCollector(stock_symbol).get_news_articles()
    stock_report = generate_news_report(stock_symbol, news_api_articles + marketaux_articles)
    stock_info = get_stock_info(stock_symbol)
    full_report = generate_stock_symbol_report(stock_symbol, stock_report, stock_info)
    return full_report


if __name__ == '__main__':
    symbols = ["BBBY", "AAPL", "TSLA", "AMZN", "MSFT", "GOOG", "VOO", "INTC", "AMD", "EA"]
    for symbol in symbols:
        try:
            report = generate_stock_report(symbol)
            with open(f'stock_report_{symbol}.json', 'w') as f:
                f.write(json.dumps(report.dict(), indent=4))
            print(report.dict())
        except Exception as e:
            print(f'Failed to generate report for {symbol} with error: {e}')

# TODO:
# Add more news sources
# About the investor & their interests & financial situation before recommending numbers.
