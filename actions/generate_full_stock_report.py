import datetime
from typing import Optional, List

from data_collection.models import NewsArticle
from data_collection.news_collection.news_api_collector import NewsAPICollector
from data_collection.stock_data_collection.company_stock_data_collector import get_stock_info, \
    get_company_name_from_symbol
from stock_analysis.models import StockSymbolReport
from stock_analysis.news_report_generator import generate_news_report
from stock_analysis.stock_symbol_report_generator import generate_stock_symbol_report


def get_stock_news(stock_symbol: str, days_ago_news: Optional[int]) -> List[NewsArticle]:
    company_name = get_company_name_from_symbol(stock_symbol)
    start_date = None
    if days_ago_news:
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days_ago_news)

    search_queries = [stock_symbol, company_name, f"{company_name} stock"]
    articles = []
    for query in search_queries:
        articles += NewsAPICollector(query).get_news_articles(num_articles=4, from_param=start_date)

    return articles


def generate_stock_report(stock_symbol: str, days_ago_news: Optional[int] = None) -> StockSymbolReport:
    stock_news = get_stock_news(stock_symbol, days_ago_news)
    # marketaux_articles = MarketauxNewsCollector(stock_symbol).get_news_articles(start_date=start_date)
    stock_report = generate_news_report(stock_symbol, stock_news)
    stock_info = get_stock_info(stock_symbol)
    full_report = generate_stock_symbol_report(stock_symbol, stock_report, stock_info)
    return full_report
