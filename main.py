import concurrent.futures
from typing import List

import typer
from rich.console import Console

from actions.generate_full_stock_report import generate_full_stock_report
from common.models.export_type import ExportType
from common.models.stock_analysis import StockSymbolReport
from config import MAX_REPORT_FETCHING_THREADS
from db.get_stock_symbol_reports import get_all_stock_symbol_reports, get_most_recent_stock_symbol_reports
from export.export_reports import export_stock_report
from export.export_reports_to_json import export_stock_symbol_report_to_json

app = typer.Typer()
console = Console()


@app.command()
def generate_stock_report(
        symbols: str = typer.Option(..., help="List of stock symbols separated by commas, like msft,aapl,amzn"),
        days_ago_news: int = typer.Option(5, help="Number of days ago to fetch news"),
        attempt_self_reflexion: bool = typer.Option(True, help="Attempt self reflexion for the report"),
        export_type: ExportType = typer.Option(ExportType.JSON, help="The type of file to export to. "
                                                                     "Can be json or pdf")):

    def get_report(stock_symbol: str) -> StockSymbolReport:
        try:
            return generate_full_stock_report(stock_symbol, days_ago_news=days_ago_news,
                                              attempt_self_reflexion=attempt_self_reflexion)
        except Exception as e:
            console.print(f"Error generating stock report for symbol: {stock_symbol}, error: {e}")
            return None

    symbols_list = symbols.split(",")
    # Upper case all symbols
    symbols_list = [symbol.upper().strip() for symbol in symbols_list]
    print(symbols_list)

    console.print(f"Generating stock reports for symbols: {', '.join(symbols_list)}")
    exported_files = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_REPORT_FETCHING_THREADS) as executor:
        futures = [executor.submit(get_report, value) for value in symbols_list]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        console.print(f"Finished Generating stock reports for symbols: {', '.join(symbols_list)}")

        for result in results:
            exported_files.append(export_stock_report(export_type, result))
    if exported_files:
        console.print(f"Exported stock reports to files: {exported_files}")


@app.command()
def get_stock_report(latest: bool = typer.Option(True, help="Show only the latest stock report for each symbol"),
                     export_type: str = typer.Option("json", help="Export type, can be json or pdf")):
    if latest:
        reports = get_most_recent_stock_symbol_reports()
    else:
        reports = get_all_stock_symbol_reports()

    exported_files = []
    for report in reports:
        exported_files.append(export_stock_report(ExportType(export_type), report))

    console.print(f"Exported stock reports to files: {exported_files}")


@app.command()
def generate_recommendations():
    console.print("Generating recommendations")
    # Implement your recommendations generation logic here


@app.command()
def export_recommendation(output_format: str = "json"):
    console.print(f"Exporting recommendation in {output_format} format")
    # Implement your recommendation export logic here


if __name__ == "__main__":
    app()
