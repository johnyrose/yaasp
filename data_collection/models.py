from pydantic import BaseModel


class NewsArticle(BaseModel):
    source: str
    title: str
    body: str
