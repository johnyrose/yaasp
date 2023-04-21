import os
import json
from datetime import datetime
from pydantic import BaseModel
from pathlib import Path

from common.logger import logger
from config import STOCK_SYMBOL_JSON_REPORTS_DIRECTORY, RECOMMENDATIONS_DIRECTORY
from common.models.recommendations import PurchaseRecommendation
from common.models.stock_analysis import StockSymbolReport


def create_directory_if_not_exists(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_filename(prefix: str) -> str:
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{current_datetime}.json"


def export_json_to_file(json_data: BaseModel, file_path: str) -> None:
    with open(file_path, 'w') as outfile:
        json.dump(json_data.dict(), outfile, indent=4)


def export_stock_symbol_report(report: StockSymbolReport) -> str:
    logger.info(f"Exporting stock symbol report for {report.stock_symbol} to JSON.")
    create_directory_if_not_exists(STOCK_SYMBOL_JSON_REPORTS_DIRECTORY)
    filename = generate_filename(f"StockSymbolReport_{report.stock_symbol}")
    file_path = Path(STOCK_SYMBOL_JSON_REPORTS_DIRECTORY) / filename
    export_json_to_file(report, file_path)
    logger.info(f"Exported stock symbol report for {report.stock_symbol} to JSON.")
    return file_path


def export_purchase_recommendation(recommendation: PurchaseRecommendation) -> None:
    logger.info(f"Exporting purchase recommendation to JSON.")
    create_directory_if_not_exists(RECOMMENDATIONS_DIRECTORY)
    filename = generate_filename("PurchaseRecommendation")
    file_path = Path(RECOMMENDATIONS_DIRECTORY) / filename
    export_json_to_file(recommendation, file_path)
    logger.info(f"Exported purchase recommendation to JSON.")
