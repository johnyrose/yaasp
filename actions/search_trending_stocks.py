import datetime
import json
from typing import List

from common.logger import logger
from common.openai_adapter import get_openai_response
from common.openai_prompts import GET_TRENDING_STOCKS
from config import OPENAI_MODEL_FOR_SIMPLE_TASKS
from data_collection.models import NewsArticle
from data_collection.news_collection.news_api_collector import NewsAPICollector


def find_news_on_trending_stocks(days_ago_news: int) -> List[NewsArticle]:
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days_ago_news)
    search_queries = [
        'stock market',
        'trending stocks',
        'stocks to watch'
    ]
    articles = []
    for query in search_queries:
        articles += NewsAPICollector(query).get_news_articles(num_articles=4, from_param=start_date)
    return articles


def search_trending_stocks(days_ago_news: int = 2) -> List[str]:
    articles = find_news_on_trending_stocks(days_ago_news)
    prompt = GET_TRENDING_STOCKS.format(
        articles=articles
    )
    retry_count = 4  # TODO - Make this configurable
    for i in range(retry_count):
        try:
            response = get_openai_response(prompt, OPENAI_MODEL_FOR_SIMPLE_TASKS)
            response_json = json.loads(response)
            return response_json
        except Exception as e:
            logger.warning(f"Failed to search trending stocks the following error was received: {e}. Retrying...")
    raise Exception("Failed to search trending stocks")