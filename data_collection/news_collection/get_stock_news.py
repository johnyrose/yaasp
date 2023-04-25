import datetime
from typing import List

from common.logger import logger
from common.models.data_collection import NewsArticle
from config import NEWS_SOURCES_TO_USE
from data_collection.news_collection.marketaux_collector import MarketauxNewsCollector
from data_collection.news_collection.news_api_collector import NewsAPICollector
from data_collection.stock_data_collection.company_stock_data_collector import get_company_name_from_symbol
from itertools import cycle

news_sources_mapping = {
    "newsapi": NewsAPICollector,
    "marketaux": MarketauxNewsCollector
}


def is_stock_index(stock_symbol: str) -> bool:
    # TODO - Yes, obviously this needs to be improved, but it's good enough for now
    index_symbols = ["VOO", "SPY", "QQQ", "DIA"]
    return stock_symbol.upper() in index_symbols


def get_news_for_queries(queries: List[str], days_ago_news: int = 5) -> List[NewsArticle]:
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days_ago_news)

    articles = []

    for query, source in zip(queries, cycle(NEWS_SOURCES_TO_USE)):
        collector_class = news_sources_mapping.get(source.strip())
        try:
            collector = collector_class(query)
            logger.info(f"Getting news for {query} from {source}")
            articles += collector.get_news_articles(num_articles=4, from_param=start_date)
        except Exception as e:
            logger.warning(f"Failed to get news for {query} from {source} with the following error: {e}")
            continue

    return articles


def get_stock_news(stock_symbol: str, days_ago_news: int = 5) -> List[NewsArticle]:

    # Check for unknown news sources
    for source in NEWS_SOURCES_TO_USE:
        if source.strip() not in news_sources_mapping:
            raise ValueError(f"Unknown news source: {source}")

    if is_stock_index(stock_symbol):
        search_queries = [stock_symbol]
    else:
        company_name = get_company_name_from_symbol(stock_symbol)
        search_queries = [stock_symbol, company_name, f"{company_name} stock"]

    return get_news_for_queries(search_queries, days_ago_news)
