from pydantic import BaseModel
import enum


class OpenAIModelType(enum.Enum):
    GPT_35_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"


class GeneralSentiment(str, enum.Enum):
    VERY_POSITIVE = "VERY POSITIVE"
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"
    VERY_NEGATIVE = "VERY NEGATIVE"


class StockNewsReport(BaseModel):
    stock_symbol: str
    news_summary: str
    financial_information: str  # Any interesting points that can be gathered specifically in the financial sector
    general_sentiment: GeneralSentiment
    sentiment_reason: str
