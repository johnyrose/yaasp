import json
from typing import Dict

from openai_prompts import GET_FULL_STOCK_REPORT
from stock_analysis.models import StockNewsReport, StockSymbolReport, OpenAIModelType
from datetime import datetime

from stock_analysis.openai_adapter import get_openai_response


def generate_stock_symbol_report(stock_symbol: str, news_report: StockNewsReport,
                                 stock_data: Dict) -> StockSymbolReport:
    print(f"Generating stock symbol report for {stock_symbol}...")
    prompt = GET_FULL_STOCK_REPORT.format(
        date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        stock_symbol=stock_symbol,
        stock_info=stock_data,
        news_summary=news_report.news_summary
    )
    openai_response = get_openai_response(prompt, OpenAIModelType.GPT_4)
    response_json = json.loads(openai_response)
    return StockSymbolReport(**response_json)

