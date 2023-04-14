from typing import Dict, List

from pydantic import BaseModel
import enum


class OpenAIModelType(enum.Enum):
    GPT_35_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"


class StockRecommendation(str, enum.Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"


class PositionRecommendation(str, enum.Enum):
    LONG = "LONG"  # Suggest entering a long position for the stock
    SHORT = "SHORT"  # Suggest entering a short position for the stock
    NONE = "NONE"  # Suggest not to enter any position for the stock


class GeneralSentiment(str, enum.Enum):
    VERY_POSITIVE = "VERY POSITIVE"
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"
    VERY_NEGATIVE = "VERY NEGATIVE"


class ArticleSummary(BaseModel):
    summary: str
    date: str


class StockNewsReport(BaseModel):
    stock_symbol: str
    news_summary: str
    financial_information: str  # Any interesting points that can be gathered specifically in the financial sector
    general_sentiment: GeneralSentiment
    sentiment_reason: str
    articles_summary: List[ArticleSummary]


class StockSymbolReport(BaseModel):
    stock_symbol: str
    news_report: StockNewsReport  # The news report for the stock symbol
    data: Dict  # The data for the stock symbol
    stock_recommendation: StockRecommendation  # The recommendation for the stock
    stock_recommendation_reason: str  # The reason for the stock recommendation
    position_recommendation: PositionRecommendation  # The recommendation for the position
    position_recommendation_reason: str  # The reason for the position recommendation
    amount_suggested: int  # The amount of stocks suggested to buy/sell
    confidence_level: int  # A number from 1 to 10, 10 being the highest confidence level. This is how confident the
    # model is in its recommendation.
    confidence_explanation: str  # An explanation of the confidence level
