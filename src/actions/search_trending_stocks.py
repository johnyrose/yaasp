import datetime
import json
from typing import List, Optional

from src.common.logger import logger
from src.common.openai_adapter import get_openai_response
from src.common.openai_prompts import GET_TRENDING_STOCKS
from config import SEARCHING_FOR_TRENDING_STOCKS_MODEL
from src.common.models.data_collection import NewsArticle
from src.data_collection.news_collection.get_stock_news import get_news_for_queries


def find_news_on_trending_stocks(days_ago_news: int, free_text: Optional[str] = None) -> List[NewsArticle]:
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days_ago_news)
    if not free_text:
        search_queries = [
            'stock market',
            'trending stocks',
            'stocks to watch'
        ]
    else:
        search_queries = [
            free_text,
            f'{free_text} stocks',
        ]
    logger.info(f"Searching for news on trending stocks from {start_date} to {end_date} with queries: {search_queries}")
    articles = get_news_for_queries(search_queries, days_ago_news)
    return articles


def search_trending_stocks(days_ago_news: int = 2, free_text: Optional[str] = None) -> List[str]:
    articles = find_news_on_trending_stocks(days_ago_news, free_text)
    prompt = GET_TRENDING_STOCKS.format(
        articles=articles
    )
    retry_count = 4  # TODO - Make this configurable
    for i in range(retry_count):
        try:
            response = get_openai_response(prompt, SEARCHING_FOR_TRENDING_STOCKS_MODEL)
            response_json = json.loads(response)
            return response_json
        except Exception as e:
            logger.warning(f"Failed to search trending stocks the following error was received: {e}. Retrying...")
    raise Exception("Failed to search trending stocks")
