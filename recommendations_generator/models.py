from enum import Enum
from typing import List

from pydantic import BaseModel


class RiskPreference(str, Enum):
    RISKY = "RISKY"
    MODERATE = "MODERATE"
    SAFE = "SAFE"


class StockRecommendation(BaseModel):
    symbol: str
    target_price: float
    position: str
    amount: int
    explanation: str


class PurchaseRecommendation(BaseModel):
    stock_recommendations: List[StockRecommendation]
    explanation: str
    confidence_level: int  # A number from 1 to 10, 10 being the highest confidence level.
    # This is how confident the model is in its recommendation.
