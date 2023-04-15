import json
from typing import List

from common.logger import logger
from common.openai_adapter import get_openai_response
from common.shorten_report import get_shortened_stock_symbol_report
from config import OPENAI_MODEL_FOR_COMPLICATED_TASKS
from openai_prompts import GET_STOCK_RECOMMENDATION
from recommendations_generator.models import RiskPreference, PurchaseRecommendation
from stock_analysis.models import StockSymbolReport


def get_recommendations(stock_reports: List[StockSymbolReport], current_situation: str,
                        risk_preference: RiskPreference = RiskPreference.MODERATE) -> PurchaseRecommendation:
    """
    Generates recommendations for the given stock reports.
    :param stock_reports: The stock reports to generate recommendations for
    :param current_situation: The current situation of the user, represented by free text at the moment.
    :param risk_preference: The risk preference of the user
    """
    logger.info(f"Getting recommendations for provided stock reports.")
    retry_amount = 4
    stock_reports = [get_shortened_stock_symbol_report(stock_report) for stock_report in stock_reports]
    # TODO - Remove this when the stock reports are written shorter in the first place
    for i in range(retry_amount):
        try:
            prompt = GET_STOCK_RECOMMENDATION.format(stock_reports=stock_reports, current_situation=current_situation,
                                                     risk_preference=risk_preference)
            response = get_openai_response(prompt, model_type=OPENAI_MODEL_FOR_COMPLICATED_TASKS)
            response_json = json.loads(response)
            logger.info(f"Got recommendations for stock reports. Recommendations: {response_json}")
            return PurchaseRecommendation(**response_json)
        except Exception as e:
            logger.error(f"Failed to get recommendations for stock reports: {stock_reports}. Error: {e}. Retrying...")
    raise Exception(f"Failed to get recommendations for stock reports: {stock_reports} after {retry_amount} retries.")
