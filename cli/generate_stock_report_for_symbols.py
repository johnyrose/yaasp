import concurrent.futures
from typing import List

from rich import console

from actions.generate_full_stock_report import generate_full_stock_report
from common.models.export_type import ExportType
from common.models.stock_analysis import StockSymbolReport
from config import MAX_REPORT_FETCHING_THREADS
from export.export_reports import export_stock_report


def generate_stock_report_for_symbols(symbols: List[str], days_ago_news: int, attempt_self_reflexion: bool,
                                      export_type: str) -> List[str]:

    def get_report(stock_symbol: str) -> StockSymbolReport:
        try:
            return generate_full_stock_report(stock_symbol, days_ago_news=days_ago_news,
                                              attempt_self_reflexion=attempt_self_reflexion)
        except Exception as e:
            console.print(f"Error generating stock report for symbol: {stock_symbol}, error: {e}")
            return None

    exported_files = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_REPORT_FETCHING_THREADS) as executor:
        futures = [executor.submit(get_report, value) for value in symbols]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

        for result in results:
            try:
                exported_files.append(export_stock_report(ExportType(export_type.upper()), result))
            except Exception as e:
                console.print(f"Error exporting stock report for symbol: {result.stock_symbol}, error: {e}")

    return exported_files
