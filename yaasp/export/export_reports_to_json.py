import os
import json
from pydantic import BaseModel
from pathlib import Path

from yaasp.common.logger import logger
from yaasp.config import STOCK_SYMBOL_REPORTS_DIRECTORY, RECOMMENDATIONS_DIRECTORY
from yaasp.common.models.recommendations import PurchaseRecommendation
from yaasp.common.models.stock_analysis import StockSymbolReport


def create_directory_if_not_exists(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)


def export_json_to_file(json_data: BaseModel, file_path: str) -> None:
    with open(file_path, 'w') as outfile:
        json.dump(json_data.dict(), outfile, indent=4)


def export_stock_symbol_report_to_json(report: StockSymbolReport) -> str:
    logger.info(f"Exporting stock symbol report for {report.stock_symbol} to JSON.")
    create_directory_if_not_exists(STOCK_SYMBOL_REPORTS_DIRECTORY)
    filename = f"StockSymbolReport_{report.stock_symbol}_{report.timestamp.replace(' ', '-')}.json"
    file_path = Path(STOCK_SYMBOL_REPORTS_DIRECTORY) / filename
    export_json_to_file(report, file_path)
    logger.info(f"Exported stock symbol report for {report.stock_symbol} to JSON.")
    return str(file_path)


def export_purchase_recommendation_to_json(recommendation: PurchaseRecommendation) -> str:
    logger.info(f"Exporting purchase recommendation to JSON.")
    create_directory_if_not_exists(RECOMMENDATIONS_DIRECTORY)
    filename = f"PurchaseRecommendation_{recommendation.timestamp.replace(' ', '-')}.json"
    file_path = Path(RECOMMENDATIONS_DIRECTORY) / filename
    export_json_to_file(recommendation, file_path)
    logger.info(f"Exported purchase recommendation to JSON.")
    return str(file_path)
