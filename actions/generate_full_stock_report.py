from data_collection.news_collection.marketaux_collector import MarketauxNewsCollector
from data_collection.news_collection.news_api_collector import NewsAPICollector
from data_collection.stock_data_collection.company_stock_data_collector import get_stock_info
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