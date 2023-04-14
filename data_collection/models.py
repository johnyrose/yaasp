from pydantic import BaseModel


class NewsArticle(BaseModel):
    source: str
    title: str
    body: str
    date: str


class CompanyStockInfo(BaseModel):
    symbol: str
    description: str
    bid: float
    ask: float
    last: float
    change: float
    days_range: str
    fifty_two_week_range: str
    volume: int
    avg_volume: int
    market_cap: int
    pe_ratio: float
    eps: float
    earnings_date: str
    dividend: float
    dividend_yield: float
    ex_dividend_date: str
    one_year_target_estimate: float
