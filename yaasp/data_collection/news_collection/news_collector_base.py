from typing import List

from yaasp.common.models.data_collection import NewsArticle


class NewsCollectorBase:
    def __init__(self, query: str):
        self.query = query

    def get_news_articles(self, num_articles: int = 5, *args, **kwargs) -> List[NewsArticle]:
        raise NotImplementedError
