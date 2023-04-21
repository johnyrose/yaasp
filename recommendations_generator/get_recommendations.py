import json
from typing import List

from common.db_utils import save_to_db
from common.logger import logger
from common.openai_adapter import get_openai_response
from common.shorten_report import get_shortened_stock_symbol_report
from config import OPENAI_MODEL_FOR_COMPLICATED_TASKS
from export.export_reports_to_json import export_purchase_recommendation
from common.openai_prompts import GET_STOCK_RECOMMENDATION
from common.models.recommendations import RiskPreference, PurchaseRecommendation
from common.models.stock_analysis import StockSymbolReport


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
            purchase_recommendation = PurchaseRecommendation(**response_json)
            save_to_db(purchase_recommendation)
            return purchase_recommendation
        except Exception as e:
            logger.error(f"Failed to get recommendations for stock reports: {stock_reports}. Error: {e}. Retrying...")
    raise Exception(f"Failed to get recommendations for stock reports: {stock_reports} after {retry_amount} retries.")
