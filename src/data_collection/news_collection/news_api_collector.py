from typing import List

from newsapi import NewsApiClient

from src.common.logger import logger
from config import NEWS_API_KEY
from src.common.models.data_collection import NewsArticle
from src.data_collection.news_collection.news_collector_base import NewsCollectorBase


class NewsAPICollector(NewsCollectorBase):
    def __init__(self, query: str):
        super().__init__(query)
        self.newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    def get_news_articles(self, num_articles: int = 5, *args, **kwargs) -> List[NewsArticle]:
        """
        Get news articles from NewsAPI

        :param num_articles: The number of articles to get
        :param args: Arguments to pass to the NewsAPI get_everything method
        :param kwargs: Keyword arguments to pass to the NewsAPI get_everything method
        :return:
        """
        articles = self.newsapi.get_everything(q=self.query, page_size=num_articles, *args, **kwargs)
        returned_articles = []
        for article in articles['articles']:
            try:
                returned_articles.append(NewsArticle(
                    source=article['source']['name'],
                    title=article['title'],
                    body=article['description'],
                    date=article['publishedAt']
                ))
            except Exception as e:
                logger.warning(f"Failed to get article from NewsAPI with the following error: {e}. Skipping...")
        return returned_articles
