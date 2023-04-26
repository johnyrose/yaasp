from datetime import datetime
from typing import List, Dict, Optional

from pydantic import BaseModel


class NewsArticle(BaseModel):
    source: str
    title: str
    body: str
    date: str


class CompanyStockInfo(BaseModel):
    industry: str
    sector: str
    fullTimeEmployees: int
    previousClose: float
    open: float
    dayLow: float
    dayHigh: float
    regularMarketVolume: int
    marketCap: int
    fiftyTwoWeekLow: float
    fiftyTwoWeekHigh: float
    twoHundredDayAverage: float
    trailingAnnualDividendYield: float
    sharesShort: int
    heldPercentInstitutions: float
    pegRatio: float
    exchange: str
    symbol: str
    underlyingSymbol: str
    description: str
    bid: float
    ask: float
    last: float
    change: float
    days_range: str
    fifty_two_week_range: str
    volume: int
    avg_volume: int
    pe_ratio: float
    eps: float
    earnings_date: str
    dividend: float
    dividend_yield: float
    ex_dividend_date: str
    company_earnings: Optional[List[Dict]]
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
