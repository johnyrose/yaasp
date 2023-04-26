import requests
from datetime import datetime, timedelta
from typing import List, Optional

from yaasp.config import MARKETAUX_API_KEY
from yaasp.common.models.data_collection import NewsArticle
from yaasp.data_collection.news_collection.news_collector_base import NewsCollectorBase


class MarketauxNewsCollector(NewsCollectorBase):
    MARKETAUX_API_URL = "https://api.marketaux.com/v1/news/all"

    def __init__(self, query: str):
        super().__init__(query)
        self.api_key = MARKETAUX_API_KEY

    def get_news_articles(self, num_articles: int = 5, start_date: Optional[datetime] = None,
                          *args, **kwargs) -> List[NewsArticle]:
        published_after = (datetime.utcnow() - timedelta(days=200)).strftime('%Y-%m-%dT%H:%M')

        if start_date:
            published_after = start_date.strftime('%Y-%m-%dT%H:%M')

        params = {
            'filter_entities': 'true',
            'limit': num_articles,
            'published_after': published_after,
            'symbols': [self.query],
            'api_token': self.api_key,
            'language': 'en'
        }

        response = requests.get(self.MARKETAUX_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        articles = [
            NewsArticle(
                source=article['source'],
                title=article['title'],
                body=article['description'],
                date=article['published_at']
            )
            for article in data['data']
        ]

        return articles