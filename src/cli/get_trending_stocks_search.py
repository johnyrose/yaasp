from typing import Optional, List

from src.actions import search_trending_stocks


def get_trending_stocks_search(free_text: Optional[str] = None) -> List[str]:
    trending_stocks = search_trending_stocks(free_text=free_text)
    return trending_stocks
