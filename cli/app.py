import concurrent.futures
from typing import List

import typer
from rich.console import Console

from actions.generate_full_stock_report import generate_full_stock_report
from common.models.stock_analysis import StockSymbolReport
from config import MAX_REPORT_FETCHING_THREADS
from export.export_reports_to_json import export_stock_symbol_report

app = typer.Typer()
console = Console()


@app.command()
def generate_stock_report(
        symbols: List[str] = typer.Option(..., help="List of stock symbols separated by spaces, like msft aapl amzn"),
        days_ago_news: int = typer.Option(5, help="Number of days ago to fetch news"),
        attempt_self_reflexion: bool = typer.Option(True, help="Attempt self reflexion for the report"),
        export_pdf: bool = typer.Option(False, help="Export the generated reports as PDF")):
    def get_report(stock_symbol: str) -> StockSymbolReport:
        return generate_full_stock_report(stock_symbol, days_ago_news=days_ago_news,
                                          attempt_self_reflexion=attempt_self_reflexion)

    console.print(f"Generating stock reports for symbols: {', '.join(symbols)}")
    exported_files = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_REPORT_FETCHING_THREADS) as executor:
        futures = [executor.submit(get_report, value) for value in symbols]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        console.print(f"Finished Generating stock reports for symbols: {', '.join(symbols)}")

        if export_pdf:
            for result in results:
                exported_files.append(export_stock_symbol_report(result))
    if exported_files:
        console.print(f"Exported stock reports to files: {exported_files}")


@app.command()
def get_stock_report(search_by: str = "", latest: bool = False):
    console.print(f"Getting stock report with search_by: {search_by}, latest: {latest}")
    # Implement your get stock report logic here


@app.command()
def generate_recommendations():
    console.print("Generating recommendations")
    # Implement your recommendations generation logic here


@app.command()
def export_stock_report(symbols: str, output_format: str = "json"):
    console.print(f"Exporting stock report for symbols: {symbols} in {output_format} format")
    # Implement your stock report export logic here


@app.command()
def export_recommendation(output_format: str = "json"):
    console.print(f"Exporting recommendation in {output_format} format")
    # Implement your recommendation export logic here


if __name__ == "__main__":
    app()
