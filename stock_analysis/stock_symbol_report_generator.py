import json
from typing import Dict

from common.logger import logger
from config import OPENAI_MODEL_FOR_COMPLICATED_TASKS
from data_collection.models import CompanyStockInfo
from openai_prompts import GET_FULL_STOCK_REPORT
from stock_analysis.models import StockNewsReport, StockSymbolReport
from datetime import datetime

from common.openai_adapter import get_openai_response


def generate_stock_symbol_report(stock_symbol: str, news_report: StockNewsReport,
                                 stock_data: CompanyStockInfo) -> StockSymbolReport:
    logger.info(f"Generating stock symbol report for {stock_symbol}...")
    prompt = GET_FULL_STOCK_REPORT.format(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        stock_symbol=stock_symbol,
        stock_info=stock_data,
        news_summary=news_report.news_summary
    )
    retry_count = 4  # TODO - Make this configurable
    for i in range(retry_count):
        try:
            openai_response = get_openai_response(prompt, OPENAI_MODEL_FOR_COMPLICATED_TASKS)
            response_json = json.loads(openai_response)
            response_json["news_report"] = news_report
            response_json["data"] = stock_data
            logger.info(f"Generated stock symbol report for {stock_symbol}. Report: {response_json}")
            return StockSymbolReport(**response_json)
        except Exception as e:
            logger.error(f"Failed to generate stock symbol report for {stock_symbol} the following error was received: "
                         f"{e}. Retrying...")
    raise Exception("Failed to generate stock symbol report")

